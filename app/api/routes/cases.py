# coordinates database (crud),  AI (LegalAnalysisService), and  external web scraper (KanoonService).

import traceback  #for tracing error 
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Query, status
from app.api.dependencies import get_db_session, get_legal_service, get_kanoon_service
from app.errors import user_not_found_exc, case_not_found_exc, server_error_exc
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.models.schemas import CaseRequest, CaseResponse, CaseRead, CaseSummaryApproveRequest, ChargesActionRequest, NewChargeRequest
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection
from app.services.legal_service import LegalAnalysisService
from app.services.kanoon_service import KanoonService
from sqlalchemy import delete
from sqlalchemy.future import select # Ensure this is imported at the top!


# FIXED: Prefix handles the "/cases" part, so the route below just needs ""
# This groups all the routes in this file under the /cases URL
router = APIRouter(prefix="/cases", tags=["Legal Cases"])



@router.get(
    "", 
    response_model=List[CaseRead], # Returns a LIST of your Pydantic schemas
    status_code=status.HTTP_200_OK,
    summary="Fetch all cases for a specific user"
)
async def get_user_cases(
    user_id: UUID, # Requires the client to pass the user ID in the URL
    # NEW: Add the search query parameter. Default is None if they aren't searching.
    search: str | None = Query(None, description="Search by case title or description"),
    skip: int = Query(0, ge=0, description="How many records to skip"),
    limit: int = Query(100, ge=1, le=100, description="How many records to return"),
    db: AsyncSession = Depends(get_db_session)
):
    try:
        # LOGIC STEP 1: Verify the user actually exists
        user = await crud.user.get(db, id=user_id)  # TODO: will be authorised by the authentication Decorator
        if not user:
            raise user_not_found_exc()

        # LOGIC STEP 2: Fetch the paginated cases
        cases = await crud.legal_case.get_multi_by_user(
            db=db, user_id=user_id, skip=skip, limit=limit, search=search
        )

        # Because you set response_model=List[CaseResponse], 
        # FastAPI will automatically format the raw database objects into secure JSON!
        return cases

    except Exception as e:
        print("🚨 FETCH ERROR 🚨")
        traceback.print_exc()
        raise server_error_exc(e)
    



# ==========================================
# PHASE 1: INTAKE & DRAFT SUMMARY
# ==========================================
@router.post(
    "", 
    response_model=CaseRead, # Returns the saved DB object
    status_code=status.HTTP_201_CREATED,
    summary="Phase 1: Draft case summary (Pending Review)"
)
async def create_draft_case(
    request: CaseRequest,
    db: AsyncSession = Depends(get_db_session),
    legal_service: LegalAnalysisService = Depends(get_legal_service)
):
    try:
        # 1. Verify user
        user = await crud.user.get(db, id=request.user_id)
        if not user:
            raise user_not_found_exc()

        # 2. Call Groq ONLY for the summary and title
        print("🚀 Calling Groq for Draft Summary...")
        draft_result = await legal_service.draft_summary(case_description=request.case_description)

        # 3. Save as "pending_review"
        db_case = LegalCase(
            user_id=request.user_id,
            title=draft_result.title,
            raw_description=request.case_description,
            llm_summary=draft_result.summary,
            status="pending_review"
        )
        db.add(db_case)
        await db.commit()
        await db.refresh(db_case)

        return db_case

    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR IN PHASE 1 🚨")
        traceback.print_exc()
        raise server_error_exc(e)
    


# ==========================================
# PHASE 2: APPROVE SUMMARY & EXTRACT CHARGES
# ==========================================
@router.put(
    "/{case_id}/extract-charges", 
    status_code=status.HTTP_200_OK,
    summary="Phase 2: Approve summary and let AI extract draft charges"
)
async def approve_summary_and_extract(
    case_id: UUID,
    request: CaseSummaryApproveRequest, 
    db: AsyncSession = Depends(get_db_session),
    legal_service: LegalAnalysisService = Depends(get_legal_service)
):
    try:
        # 1. Fetch case
        db_case = await crud.legal_case.get(db, id=case_id)
        if not db_case:
            raise case_not_found_exc()

        # 2. Save the lawyer's approved summary
        db_case.lawyer_approved_summary = request.lawyer_approved_summary
        
        # 3. Call Groq to extract charges
        print("🚀 Calling Groq for IPC Extraction...")
        charges = await legal_service.extract_charges(approved_summary=request.lawyer_approved_summary)

        # 4. Save DRAFT charges to DB
        if charges:
            for charge in charges:
                db_section = LegalSection(
                    case_id=db_case.id,
                    ipc_section=charge.ipc_section,
                    bns_section=charge.bns_equivalent,
                    reason=charge.explanation,
                    source="LLM"
                )
                db.add(db_section)

        # 5. Update status so the frontend knows it's waiting on charge approval
        db_case.status = "pending_charge_review"
        await db.commit()

        return {"message": "Charges extracted successfully", "draft_charges": charges}

    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR IN PHASE 2 🚨")
        traceback.print_exc()
        raise server_error_exc(e)

# ==========================================
# PHASE 3: FINALIZE CHARGES & FETCH KANOON
# ==========================================
@router.put(
    "/{case_id}/finalize", 
    response_model=CaseResponse, 
    status_code=status.HTTP_200_OK,
    summary="Phase 3: Finalize lawyer-approved charges and fetch Kanoon precedents"
)
async def finalize_charges_and_fetch_kanoon(
    case_id: UUID,
    request: ChargesActionRequest, 
    db: AsyncSession = Depends(get_db_session),
    kanoon_service: KanoonService = Depends(get_kanoon_service)
):
    try:
        db_case = await crud.legal_case.get(db, id=case_id)
        if not db_case:
            raise case_not_found_exc()

        # 1. Fetch ALL existing draft charges for this case
        query = select(LegalSection).where(LegalSection.case_id == case_id)
        result = await db.execute(query)
        existing_charges = result.scalars().all()

        # Optimize lookups for the loops below
        approved_ids = set(request.approved_id or [])
        rejected_dict = {item.id: item.reason for item in (request.rejected_data or [])}

        first_approved_ipc = None
        final_db_charges = []

        # 2. Apply the lawyer's actions to the existing charges
        for charge in existing_charges:
            if charge.id in approved_ids:
                # SCENARIO A: Lawyer Ticked (Approved)
                charge.is_approved = True
                charge.has_lawyer_verified = True
                
                if not first_approved_ipc:
                    first_approved_ipc = charge.ipc_section

            elif charge.id in rejected_dict:
                # SCENARIO B: Lawyer Crossed (Rejected & Provided Reason)
                charge.is_approved = False
                charge.has_lawyer_verified = True
                charge.reason = rejected_dict[charge.id] # Overwrite with lawyer's rejection reason

            else:
                # SCENARIO C: Cleanup (Orphan handling)
                if charge.source == "LLM":
                    # If an AI draft is missing from the approved list, it was rejected.
                    charge.is_approved = False
                    charge.has_lawyer_verified = True
                elif charge.source == "LAWYER_MANUAL":
                    # If a manual charge is missing from the lists, leave it alone! 
                    # It stays approved. We just need to catch it for Kanoon.
                    if charge.is_approved and not first_approved_ipc:
                        first_approved_ipc = charge.ipc_section
            db.add(charge)
            final_db_charges.append(charge)

        # 3. Call Kanoon API using the FIRST Ticked/Approved charge
        precedents = []
        
        # 1. Extract ONLY the IPC sections that are actively approved
        approved_sections = [
            charge.ipc_section 
            for charge in final_db_charges 
            if charge.is_approved
        ]
        
        if approved_sections:
            # OPTIMIZATION: If they approve 10 charges, an "AND" search for all 10 
            # might return 0 results because it's too strict. 
            # It's best practice to search using the top 2 or 3 primary charges.
            top_sections = approved_sections[:3] 
            
            # 2. Chain them together: '"Section 441" AND "Section 383"'
            combined_sections = " AND ".join([f'"{sec}"' for sec in top_sections])
            
            # 3. Add the "IPC" keyword to narrow it to penal code rulings
            search_query = f'({combined_sections}) AND "IPC"' 
            
            print(f"🚀 Calling Kanoon API for combined query: {search_query}...")
            precedents = await kanoon_service.fetch_precedents(search_query=search_query)

        # 4. Mark the case as completed
        db_case.status = "completed"
        await db.commit()

        # 5. Format output
        clean_charges = [
            {
                "ipc_section": charge.ipc_section,
                "bns_equivalent": charge.bns_section, 
                "offense": "Refer to IPC",            
                "explanation": charge.reason,         
                "id": charge.id,
                "is_approved": charge.is_approved
            } 
            for charge in final_db_charges
            if charge.is_approved
        ]

        return CaseResponse(
            case_summary=db_case.lawyer_approved_summary,
            applicable_charges=clean_charges,
            precedent_cases=precedents
        )

    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR IN PHASE 3 🚨")
        traceback.print_exc()
        raise server_error_exc(e)
    


# ==========================================
# PHASE 2.5: ADD MANUAL CHARGE
# ==========================================
@router.post(
    "/{case_id}/charges", 
    status_code=status.HTTP_201_CREATED,
    summary="Add a new manual charge to a case"
)
async def add_manual_charge(
    case_id: UUID,
    request: NewChargeRequest, 
    db: AsyncSession = Depends(get_db_session)
):
    try:
        db_case = await crud.legal_case.get(db, id=case_id)
        if not db_case:
            raise case_not_found_exc()

        # Create the brand new manual charge
        new_charge = LegalSection(
            case_id=case_id,
            ipc_section=request.ipc_section,
            bns_section=request.bns_section,
            reason=request.reason,
            source="LAWYER_MANUAL",
            is_approved=True, # It's manual, so it starts approved
            has_lawyer_verified=True
        )
        
        db.add(new_charge)
        await db.commit()
        await db.refresh(new_charge)

        return {
            "message": "Charge added successfully",
            "charge": {
                "id": new_charge.id,
                "ipc_section": new_charge.ipc_section,
                "bns_equivalent": new_charge.bns_section,
                "explanation": new_charge.reason,
                "is_approved": new_charge.is_approved
            }
        }

    except Exception as e:
        await db.rollback()
        traceback.print_exc()
        raise server_error_exc(e)