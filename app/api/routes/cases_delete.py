from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.Dependencies.auth import get_current_user
from app.models.user import User
from app.api.dependencies import get_db_session
from app.controllers import delete_case_controller

router = APIRouter()


@router.delete(
    "/{case_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft delete a legal case and its associated charges",
)
async def delete_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_case_controller(
        case_id,
        current_user,
        db,
    )
