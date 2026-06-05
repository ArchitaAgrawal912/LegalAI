from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.database import get_session
from app.serializers.ai_serializer import CaseAnalysisResponse, CaseAnalysisRequest

# 🎯 Sirf ek Controller import kiya
from app.controllers.llm_summary import generate_summary_and_save 

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.post("/generate-summary", response_model=CaseAnalysisResponse)
def api_generate_case_summary(
    request: CaseAnalysisRequest, 
    session: Session = Depends(get_session)
):      
    try:
        # 1. 🧠 Controller Call: AI generation aur DB save dono ek saath ho gaye!
        saved_case = generate_summary_and_save(
            session=session,
            user_id=request.user_id,
            raw_description=request.raw_description
        )

        # 2. 🌐 Frontend Response: Seedha clean data bheja
        return CaseAnalysisResponse(
            case_id=saved_case.id,
            title=saved_case.title,
            llm_summary=saved_case.llm_summary
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating summary: {str(e)}")