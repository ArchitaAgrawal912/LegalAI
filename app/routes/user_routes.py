from fastapi import APIRouter, HTTPException
# Import your serializers and controllers
from app.serializers.user_serializer import CaseAnalysisRequest, CaseAnalysisResponse
from app.controllers.user_controller import get_legal_analysis

router = APIRouter()

@router.post("/analyze-case", response_model=CaseAnalysisResponse, tags=["Legal AI"])
async def analyze_case_endpoint(request: CaseAnalysisRequest):
    # Calling the AI controller that holds your custom prompt
    result = await get_legal_analysis(request.case_text)
    
    if not result:
        raise HTTPException(status_code=500, detail="AI processing failed. Check your API key or network.")
        
    # Return the direct dictionary, FastAPI validates it with CaseAnalysisResponse automatically
    return result