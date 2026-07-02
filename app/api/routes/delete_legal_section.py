from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.controllers.delete_legal_section import (
    delete_legal_section_controller,
)

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
):
    return await delete_legal_section_controller(
        case_id=case_id,
        section_id=section_id,
        db=db,
    )