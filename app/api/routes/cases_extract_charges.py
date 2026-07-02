from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session, get_legal_service
from app.schemas.case import CaseSummaryApproveRequest
from app.services.legal_service import LegalAnalysisService
from app.controllers import approve_summary_and_extract_controller
from app.schemas.section import ExtractChargesResponse
router = APIRouter()


@router.put(
    "/{case_id}/extract-charges",
    status_code=status.HTTP_200_OK,
    summary="Phase 2: Approve summary and let AI extract draft charges",
    response_model=ExtractChargesResponse
)
async def approve_summary_and_extract(
    case_id: UUID,
    request: CaseSummaryApproveRequest,
    db: AsyncSession = Depends(get_db_session),
    legal_service: LegalAnalysisService = Depends(get_legal_service),
):
   result =   return await approve_summary_and_extract_controller(
        case_id, request, db, legal_service
    )
if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to approve summary and extract charges.",
        )
        
        
        #  controller se many filed comes by response model se paas hoke vhi return hone jo response model me hai , kyuki vhi fronedn ko chjye honge , 