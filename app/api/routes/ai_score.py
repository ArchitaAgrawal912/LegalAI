from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session, get_legal_service
from app.controllers.calculate_ai_score import calculate_ai_scores_controller
from app.services.legal_service import LegalAnalysisService


router = APIRouter()

@router.post(
    "/{case_id}/score-precedents", 
    status_code=status.HTTP_200_OK,
    summary="POC: Calculate AI relevance scores for all fetched precedents"
)
async def score_precedents(
    case_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    legal_service: LegalAnalysisService = Depends(get_legal_service)
):
    return await calculate_ai_scores_controller(case_id, db, legal_service)