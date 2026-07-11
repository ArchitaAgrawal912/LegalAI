from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.Dependencies.auth import get_current_user
from app.api.dependencies import get_db_session
from app.controllers.delete_legal_section import (
    delete_legal_section_controller,
)
from app.models.user import User

router = APIRouter()


@router.delete(
    "/cases/{case_id}/sections/{section_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft delete a legal section belonging to a case",
)
async def delete_legal_section(
    case_id: UUID,
    section_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_legal_section_controller(
        case_id=case_id,
        section_id=section_id,
        current_user=current_user,
        db=db,
    )