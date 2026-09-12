import traceback
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from fastapi import HTTPException, status
from app.models.user import User
from app.errors import case_not_found_exc, server_error_exc
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection


async def delete_case_controller(
    case_id: UUID,
    current_user: User,
    db: AsyncSession,
):
    try:
        # 1. Fetch the case (Ensuring it isn't already deleted)
        query = select(LegalCase).where(
            LegalCase.id == case_id, LegalCase.is_deleted == False
        )
        result = await db.execute(query)
        db_case = result.scalar_one_or_none()

        if not db_case:
            raise case_not_found_exc()
        if db_case.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this case.",
            )

        # 2. Soft delete the parent case
        db_case.is_deleted = True

        # 3. CASCADE: Soft delete all associated IPC sections efficiently
        # This bulk update is faster and ignores the NULL/False trap
        await db.execute(
            update(LegalSection)
            .where(LegalSection.case_id == case_id)
            .values(is_deleted=True)
        )

        # 4. Commit the changes
        await db.commit()

        return {"message": "Case and associated data successfully deleted."}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR DURING CASE DELETION 🚨")
        traceback.print_exc()
        raise server_error_exc(e)
