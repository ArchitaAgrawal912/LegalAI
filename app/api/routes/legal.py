from fastapi import APIRouter, Depends, HTTPException, status
from functools import lru_cache
from app.models.schemas import CaseRequest, CaseResponse
from app.services.legal_service import LegalAnalysisService

router = APIRouter(prefix="/legal", tags=["Legal Intelligence"])

@lru_cache()
def get_legal_service() -> LegalAnalysisService:
    """Dependency injection to reuse the service instance across requests."""
    return LegalAnalysisService()

@router.post(
    "/analyze", 
    response_model=CaseResponse, 
    status_code=status.HTTP_200_OK,
    summary="Extract IPC and BNS sections from case facts"
)
async def analyze_incident(
    request: CaseRequest,
    legal_service: LegalAnalysisService = Depends(get_legal_service)
):
    try:
        result = await legal_service.analyze_case(case_description=request.case_description)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )