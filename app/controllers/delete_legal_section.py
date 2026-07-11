import traceback
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.errors import case_not_found_exc, server_error_exc
from app.models.legal_section import LegalSection
from app.models.user import User


async def delete_legal_section_controller(
    case_id: UUID,
    section_id: UUID,
    current_user: User,
    db: AsyncSession,
):
    try:
        # 1. Verify case exists
        db_case = await crud.legal_case.get(db, id=case_id)

        if not db_case:
            raise case_not_found_exc()

        # 2. Ownership check
        if db_case.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this section.",
            )

        # 3. Find the section belonging to this case
        query = (
            select(LegalSection)
            .where(
                LegalSection.case_id == case_id,
                LegalSection.id == section_id,
                LegalSection.is_deleted == False,
            )
        )

        result = await db.execute(query)
        db_section = result.scalar_one_or_none()

        if not db_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Legal section not found for this case.",
            )

        # 4. Soft delete
        db_section.is_deleted = True

        await db.commit()

        return {
            "message": "Legal section deleted successfully."
        }

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()

        print("🚨 CRITICAL ERROR DURING LEGAL SECTION DELETION 🚨")
        traceback.print_exc()

        raise server_error_exc(e)
    
    
    # app/controllers/delete_legal_section.py we used this , bcs yha query ke baad hume ek hi row milegi ya 0 milegi agar section id to be deleted is not in tabele