import traceback
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import crud
from app.errors import case_not_found_exc, server_error_exc
from app.models.legal_section import LegalSection
from app.models.precedent import PrecedentCase
from app.models.user import User
from app.schemas.case import CaseResponse
from app.services.kanoon_service import KanoonService
from app.services.similarity_service import compute_similarity_percentage
from app.services.llm_similarity_service import llm_similarity_scores


async def fetch_and_store_precedents_controller(
    case_id: UUID,
    current_user: User,
    db: AsyncSession,
    kanoon_service: KanoonService,
):
    try:

        # ==========================================
        # Fetch Case
        # ==========================================
        db_case = await crud.legal_case.get(db, id=case_id)

        if not db_case:
            raise case_not_found_exc()

        if db_case.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this case.",
            )

        # ==========================================
        # Fetch Approved Charges
        # ==========================================
        result = await db.execute(
            select(LegalSection).where(
                LegalSection.case_id == case_id,
                LegalSection.is_approved == True,
            )
        )

        approved_db_charges = result.scalars().all()

        if not approved_db_charges:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action denied: The lawyer must approve at least one IPC section before fetching precedents.",
            )

        approved_sections = [
            charge.ipc_section
            for charge in approved_db_charges
        ]

        # ==========================================
        # Search Indian Kanoon
        # ==========================================
        top_sections = approved_sections[:3]

        combined_sections = " AND ".join(
            f'"{sec}"'
            for sec in top_sections
        )

        search_query = f'({combined_sections}) AND "IPC"'

        print(f"🚀 Kanoon Search Query : {search_query}")

        kanoon_results = await kanoon_service.fetch_precedents(
            search_query=search_query
        )

        # ==========================================
        # Remove old precedents
        # ==========================================
        await db.execute(
            delete(PrecedentCase).where(
                PrecedentCase.case_id == case_id
            )
        )

        precedents: list[PrecedentCase] = []

        llm_queue = []

        # ==========================================
        # Embedding Similarity
        # ==========================================
        for item in kanoon_results:

            kanoon_url = (
                f"https://indiankanoon.org/doc/{item.doc_id}/"
            )

            precedent_text = (
                getattr(item, "snippet", "")
                or item.title
            )

            embedding_score = compute_similarity_percentage(
                current_case_text=db_case.raw_description,
                precedent_case_text=precedent_text,
            )

            print(
                f"{item.title[:50]} -> Embedding Score : {embedding_score}"
            )

            # Embedding confident enough
            if 30 <= embedding_score <= 70:

                precedents.append(
                    PrecedentCase(
                        case_id=db_case.id,
                        title=item.title,
                        doc_id=item.doc_id,
                        doc_url=kanoon_url,
                        ai_score=embedding_score,
                    )
                )

            # Needs LLM
            else:

                llm_queue.append(
                    {
                        "precedent": PrecedentCase(
                            case_id=db_case.id,
                            title=item.title,
                            doc_id=item.doc_id,
                            doc_url=kanoon_url,
                            ai_score=0,
                        ),
                        "snippet": precedent_text,
                    }
                )

        # ==========================================
        # Batch LLM Similarity
        # ==========================================
        if llm_queue:

            snippets = [
                item["snippet"]
                for item in llm_queue
            ]

            llm_scores = await llm_similarity_scores(
                current_case=db_case.raw_description,
                precedent_cases=snippets,
            )

            for queue_item, score in zip(
                llm_queue,
                llm_scores,
            ):

                queue_item["precedent"].ai_score = score

                precedents.append(
                    queue_item["precedent"]
                )

        # ==========================================
        # Save All Precedents
        # ==========================================
        if precedents:
            db.add_all(precedents)

        # ==========================================
        # Complete Case
        # ==========================================
        db_case.status = "completed"

        await db.commit()

        for precedent in precedents:
            await db.refresh(precedent)

        await db.refresh(db_case)

        # ==========================================
        # Response Charges
        # ==========================================
        clean_charges = [
            {
                "id": charge.id,
                "ipc_section": charge.ipc_section,
                "bns_equivalent": charge.bns_section,
                "offense": "Refer to IPC",
                "explanation": charge.reason,
                "is_approved": charge.is_approved,
            }
            for charge in approved_db_charges
        ]

        # ==========================================
        # Response Precedents
        # ==========================================
        clean_precedents = [
            {
                "id": precedent.id,
                "title": precedent.title,
                "doc_id": precedent.doc_id,
                "doc_url": precedent.doc_url,
                "ai_score": precedent.ai_score,
            }
            for precedent in precedents
        ]

        clean_precedents.sort(
            key=lambda x: x["ai_score"],
            reverse=True,
        )

        return CaseResponse(
            case_summary=db_case.lawyer_approved_summary,
            applicable_charges=clean_charges,
            precedent_cases=clean_precedents,
        )

    except Exception as e:

        await db.rollback()

        print("🚨 CRITICAL ERROR IN PRECEDENT RETRIEVAL 🚨")
        traceback.print_exc()

        raise server_error_exc(e)
    
    
    #  combined_sections = " AND ".join(
                # [f'"{sec}"' for sec in top_sections]
            # ) this will add AND between sections
            
            
            
            
            
            
            # await db.execute(
            #     delete(PrecedentCase).where(
            #         PrecedentCase.case_id == case_id
            #     )
            # ) we used this deleet kyuki maan lo pehle jo precednet aaye the ab 
            #  advocate ne ek aur ipc add ki and then fetch karne ka truy kia toh pucrane precedn htao and new 
            # lao  Agar pehle precedent hi nahi hain?

# Koi problem nahi.

# Delete query simply

# 0 rows affected

# bol degi.

# Error nahi aata.



#  kanoon_url = (
                    # f"https://indiankanoon.org/doc/{item.doc_id}/"
                # )
#  ye fronend ko bhejege taaki vo click karke case padh paye
 
 
#   reverse =true mean descending sort as by default the sorting is ascending

#   i didnot get why respons echarge and response precedent made





# OLD FLOW OF THIS CONTROLLER 
# Request
#    │
#    ▼
# Fetch Case
#    │
#    ▼
# Fetch Approved IPC Sections
#    │
#    ▼
# Search Indian Kanoon
#    │
#    ▼
# Delete Old Precedents
#    │
   ▼
# FOR EACH PRECEDENT
#    │
#    ├── Compute Embedding Score
#    │
#    ├── if 30-70
#    │       │
#    │       └── Use Embedding Score
#    │
#    └── else
#            │
#            ├── Call LLM ❌ (One API call)
#            │
#            ├── Average(Embedding + LLM)
#            │
#            └── Final Score
#    │
#    ▼
# db.add(precedent)
#    │
#    ▼
# Repeat Again...
#    │
#    ▼
# Commit
#    │
#    ▼
# Return Response




# NEW CONTROLLER FLOW (Optimized)
# Request
#    │
#    ▼
# Fetch Case
#    │
#    ▼
# Fetch Approved IPC Sections
#    │
#    ▼
# Search Indian Kanoon
#    │
#    ▼
# Delete Old Precedents
#    │
#    ▼
# FOR EACH PRECEDENT
#    │
#    ├── Compute Embedding
#    │
#    ├── if 30-70
#    │       │
#    │       └── Store directly in embedding_precedents
#    │
#    └── else
#            │
#            └── Push into llm_queue
#                     │
#                     ├── snippet
#                     ├── title
#                     ├── doc_id
#                     ├── url
#                     └── precedent object


# Why This Is Better
# Old	New
# 1 Groq call per precedent	1 Groq call for all precedents
# Multiple network round trips	Single network round trip
# Waits after every precedent	Queue first, process later
# Repeated prompt construction	One prompt
# Hard to scale	Scales to N precedents easily
# O(n) LLM API calls	O(1) LLM API call

# Optimized precedent similarity scoring by introducing a queue-based batch inference pipeline, reducing multiple Groq LLM API calls into a single batched request, 
# minimizing network overhead and improving precedent retrieval latency by ~2–3× 
# while preserving score-to-record mapping.