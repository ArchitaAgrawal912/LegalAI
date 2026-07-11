from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.Dependencies.auth import get_current_user
from app.models.user import User

from app.api.dependencies import get_db_session, get_legal_service
from app.schemas.case import CaseSummaryApproveRequest
from app.schemas.section import ExtractChargesResponse
from app.services.legal_service import LegalAnalysisService
from app.controllers import approve_summary_and_extract_controller

router = APIRouter()


@router.put(
    "/{case_id}/extract-charges",
    status_code=status.HTTP_200_OK,
    summary="Phase 2: Approve summary and let AI extract draft charges",
    response_model=ExtractChargesResponse,
)
async def approve_summary_and_extract(
    case_id: UUID,
    request: CaseSummaryApproveRequest,
    db: AsyncSession = Depends(get_db_session),
    legal_service: LegalAnalysisService = Depends(get_legal_service),
    current_user: User = Depends(get_current_user),
):
    return await approve_summary_and_extract_controller(
        case_id,
        request,
        current_user,
        db,
        legal_service,
    )