import traceback
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import crud
from app.errors import case_not_found_exc, server_error_exc
from app.models.precedent import PrecedentCase
from app.models.user import User


async def get_case_precedents_controller(
    case_id: UUID,
    current_user: User,
    db: AsyncSession,
):
    try:
        # 1. Verify the parent case actually exists
        db_case = await crud.legal_case.get(db, id=case_id)

        if not db_case:
            raise case_not_found_exc()

        # 2. Verify ownership
        if db_case.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this case.",
            )

        # 3. Fetch all precedents linked to this case ID
        query = select(PrecedentCase).where(
            PrecedentCase.case_id == case_id
        )

        result = await db.execute(query)
        precedents = result.scalars().all()

        # 4. Return the list
        return precedents

    except HTTPException:
        raise

    except Exception as e:
        print("🚨 CRITICAL ERROR FETCHING PRECEDENTS 🚨")
        traceback.print_exc()
        raise server_error_exc(e)