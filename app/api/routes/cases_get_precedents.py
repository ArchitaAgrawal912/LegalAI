from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.Dependencies.auth import get_current_user
from app.api.dependencies import get_db_session
from app.controllers import get_case_precedents_controller
from app.models.user import User
from app.schemas.precedent import PrecedentRead

router = APIRouter()


@router.get(
    "/{case_id}/precedents",
    response_model=list[PrecedentRead],
    status_code=status.HTTP_200_OK,
    summary="Get all saved legal precedents for a specific case",
)
async def get_case_precedents(
    case_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await get_case_precedents_controller(
        case_id,
        current_user,
        db,
    )