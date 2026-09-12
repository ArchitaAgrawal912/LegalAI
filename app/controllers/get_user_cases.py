import traceback

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.errors import server_error_exc
from app.models.user import User


async def get_user_cases_controller(
    current_user: User,
    search: str | None,
    skip: int,
    limit: int,
    db: AsyncSession,
):
    try:
        cases = await crud.legal_case.get_multi_by_user(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            search=search,
        )

        return cases

    except Exception as e:
        print("🚨 FETCH ERROR 🚨")
        traceback.print_exc()
        raise server_error_exc(e)