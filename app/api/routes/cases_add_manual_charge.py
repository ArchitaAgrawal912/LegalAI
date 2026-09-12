from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.Dependencies.auth import get_current_user
from app.models.user import User

from app.api.dependencies import get_db_session
from app.schemas.section import NewChargeRequest
from app.controllers import add_manual_charge_controller
from app.schemas.section import AddManualChargeResponse
router = APIRouter()


@router.post(
    "/{case_id}/charges",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new manual charge to a case",
    response_model=AddManualChargeResponse,
)
async def add_manual_charge(
    case_id: UUID,
    request: NewChargeRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await add_manual_charge_controller(
        case_id=case_id,
        request=request, 
        db=db, 
        current_user=current_user
    )
