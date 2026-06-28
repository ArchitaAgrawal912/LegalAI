import traceback
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import crud
from app.errors import case_not_found_exc, server_error_exc
from app.schemas.section import ChargesActionRequest
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection

async def finalize_charges_status_controller(
    case_id: UUID, request: ChargesActionRequest, db: AsyncSession
):
    try:
        db_case = await crud.legal_case.get(db, id=case_id)
        if not db_case:
            raise case_not_found_exc()

        query = select(LegalSection).where(LegalSection.case_id == case_id)
        result = await db.execute(query)
        existing_charges = result.scalars().all()

        approved_ids = set(request.approved_id or [])
        rejected_dict = {item.id: item.reason for item in (request.rejected_data or [])}

        final_db_charges = []

        for charge in existing_charges:
            if charge.id in approved_ids:
                charge.is_approved = True
                charge.has_lawyer_verified = True
                # Agar galti se reject ho gaya tha toh tag hatao
                if charge.reason and charge.reason.startswith("REJECT_REASON:"):
                    charge.reason = charge.reason.replace("REJECT_REASON:", "").strip()

            elif charge.id in rejected_dict:
                charge.is_approved = False
                charge.has_lawyer_verified = True
                # SMART FIX: Save Rejection Reason in the existing column with a tag!
                charge.reason = f"REJECT_REASON:{rejected_dict[charge.id]}"

            db.add(charge)
            final_db_charges.append(charge)

        db_case.status = "pending_precedents"
        await db.commit()

        # UI ko response bhejne ke liye list banate hain
        clean_charges = [
            {
                "id": charge.id,
                "ipc_section": charge.ipc_section,
                "bns_equivalent": charge.bns_section,
                "offense": "Refer to IPC",
                "explanation": charge.reason.replace("REJECT_REASON:", "") if charge.reason else "",
                "is_approved": charge.is_approved,
                "rejection_reason": charge.reason.replace("REJECT_REASON:", "") if charge.reason and charge.reason.startswith("REJECT_REASON:") else None
            }
            for charge in final_db_charges
        ]

        return {
            "message": "Charges successfully locked and verified by lawyer.",
            "applicable_charges": clean_charges,
        }
    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR IN CHARGE FINALIZATION 🚨")
        traceback.print_exc()
        raise server_error_exc(e)