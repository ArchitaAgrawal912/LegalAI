from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
# 🎯 Naye imports
from app.serializers.ai_serializer import ChargeAnalysisRequest, ReferenceOnlyResponse
from app.controllers.reference_cases import generate_and_save_references
from app.utils.api_response import success_response, error_response

router = APIRouter(prefix="/references", tags=["Reference Cases"])

@router.post("/fetch")
async def api_fetch_case_references(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # 1. Controller Call (async logic)
        precedents = await generate_and_save_references(
            session=session, 
            case_id=request.case_id, 
            approved_summary=request.lawyer_approved_summary
        )
        
        # 2. Logic: Empty list handling (tumhari requirement ke hisaab se)
        if not precedents:
            return success_response(
                data=[], 
                message="No reference cases found for this summary.",
                status_code=200
            )

        # 3. Validation: Pydantic model se data validate kiya
        response_data = ReferenceOnlyResponse(
            message="Reference cases fetched successfully.",
            reference_cases=precedents
        )
        
        # 4. Standardized Success Response
        return success_response(
            data=response_data, 
            message="References fetched successfully"
        )
        
    except Exception as e:
        session.rollback() 
        
        # 5. Standardized Error Response with logic
        if "not found" in str(e).lower():
            return error_response(
                message="Reference search failed: Case not found", 
                status_code=404, 
                details=str(e)
            )
        else:
            return error_response(
                message="Reference Fetch Error", 
                status_code=500, 
                details=str(e)
            )