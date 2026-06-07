from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.serializers.ai_serializer import CaseAnalysisResponse, CaseAnalysisRequest
from app.controllers.llm_summary import generate_summary_and_save 
# 🎯 Nayi utility imports
from app.utils.api_response import success_response, error_response

router = APIRouter(prefix="/summary", tags=["Summary"])

# 🎯 response_model hataya kyunki hum custom wrapper return kar rahe hain
@router.post("/generate-summary")
def api_generate_case_summary(
    request: CaseAnalysisRequest, 
    session: Session = Depends(get_session)
):      
    try:
        # 1. Controller Call
        saved_case = generate_summary_and_save(
            session=session,
            user_id=request.user_id,
            raw_description=request.raw_description
        )

        # 2. Validation: Data ko Schema se validate kiya
        # .model_dump() lagane se ye clear ho jata hai ki hum dictionary bhej rahe hain
        response_data = CaseAnalysisResponse(
            case_id=saved_case.id,
            title=saved_case.title,
            llm_summary=saved_case.llm_summary
        ).model_dump()

        # 3. Success Response: Wrap karke bheja
        return success_response(
            data=response_data, 
            message="Summary generated successfully"
        )

    except Exception as e:
        # Rollback zaroor karna agar DB transaction fail ho raha ho
        session.rollback()
        return error_response(
            message="Error generating summary", 
            details=str(e), 
            status_code=500
        )