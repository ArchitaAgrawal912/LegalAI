from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.Dependencies.auth import get_current_user
from app.models.user import User
from app.api.dependencies import get_db_session
from app.schemas.section import ChargesActionRequest
from app.controllers import finalize_charges_status_controller
from app.schemas.section import FinalizeChargesResponse
router = APIRouter()


@router.put(
    "/{case_id}/finalize-charges",
    status_code=status.HTTP_200_OK,
    summary="Phase 3A: Save lawyer-approved and rejected charges state to database",
    response_model=FinalizeChargesResponse,
)
async def finalize_charges_status(
    case_id: UUID,
    request: ChargesActionRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await finalize_charges_status_controller(
        case_id,
        request,
        current_user,
        db,
    )
