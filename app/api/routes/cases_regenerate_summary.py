from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.Dependencies.auth import get_current_user
from app.api.dependencies import get_db_session, get_legal_service
from app.controllers.regenerate_summary_controller import regenerate_summary_controller
from app.models.user import User
from app.schemas.case import CaseRead, CaseRegenerateRequest
from app.services.legal_service import LegalAnalysisService

router = APIRouter()


@router.put(
    "/{case_id}/regenerate",
    response_model=CaseRead,
    status_code=status.HTTP_200_OK,
    summary="Regenerate an existing case summary based on an updated description",
)
async def regenerate_case_summary_endpoint(
    case_id: UUID,
    request: CaseRegenerateRequest,
    db: AsyncSession = Depends(get_db_session),
    legal_service: LegalAnalysisService = Depends(get_legal_service),
    current_user: User = Depends(get_current_user),
):
    result = await regenerate_summary_controller(
        case_id=case_id,
        new_description=request.description,
        current_user=current_user,
        db=db,
        legal_service=legal_service,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return result