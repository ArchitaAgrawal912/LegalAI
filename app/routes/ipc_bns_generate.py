from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
# 🎯 Naye imports
from app.serializers.ai_serializer import ChargeAnalysisRequest, ChargeOnlyResponse
from app.controllers.ipc_bns_generate import generate_and_save_ipc_bns
from app.utils.api_response import success_response, error_response

router = APIRouter(prefix="/charges", tags=["Charges & Sections"])

@router.post("/analyze")
def api_analyze_case_charges(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # 1. Controller Call
        ipc_list, bns_list = generate_and_save_ipc_bns(
            session=session, 
            case_id=request.case_id, 
            approved_summary=request.lawyer_approved_summary
        )
        
        # 2. Validation: Pydantic model se data validate kiya
        response_data = ChargeOnlyResponse(
            message="Charges extracted successfully.",
            ipc_sections=ipc_list,
            bns_sections=bns_list
        )
        
        # 3. Standardized Success Response
        return success_response(
            data=response_data, 
            message="Charges analyzed successfully"
        )
        
    except Exception as e:
        # 4. Rollback in case of Database errors
        session.rollback() 
        
        # 5. Standardized Error Response with logic
        if "not found" in str(e).lower():
            return error_response(
                message="Case not found", 
                status_code=404, 
                details=str(e)
            )
        else:
            # Agar koi random system error hai, toh 500 bhej do
            return error_response(
                message="Internal Server Error", 
                status_code=500, 
                details=str(e)
            )
    