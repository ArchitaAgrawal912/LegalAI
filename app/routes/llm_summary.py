from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.database import get_session
from app.serializers.ai_serializer import CaseAnalysisResponse, CaseAnalysisRequest
from app.controllers.llm_summary import generate_summary_from_llm
from app.models.crud import create_case_with_summary # 🎯 CRUD wala function import kiya

# @router waali line teri file me pehle se hogi
router = APIRouter(prefix="/summary", tags=["Summary"])

@router.post("/generate-summary", response_model=CaseAnalysisResponse)
def api_generate_case_summary(
    request: CaseAnalysisRequest, 
    session: Session = Depends(get_session)
):      
    try:
        # 1. 🧠 Controller Call: LLM se Title aur Summary laana
        llm_data = generate_summary_from_llm(request.raw_description)
        
        title = llm_data.get("title", "Untitled Case")
        llm_summary = llm_data.get("llm_summary", request.raw_description)
        
        # 2. 🗄️ Database Call: CRUD function ko use karke case save karna
        new_case = create_case_with_summary(
            session=session,
            user_id=request.user_id,
            raw_description=request.raw_description,
            title=title,
            llm_summary=llm_summary
        )

        # 3. 🌐 Frontend Response: Clean response return karna
        return CaseAnalysisResponse(
            case_id=new_case.id,
            title=new_case.title,
            llm_summary=new_case.llm_summary
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating summary: {str(e)}")