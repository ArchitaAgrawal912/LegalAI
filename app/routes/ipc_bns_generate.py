from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.database import get_session
from app.serializers.ai_serializer import ChargeAnalysisRequest, ChargeAnalysisResponse

# 🎯 SIRF EK CONTROLLER IMPORT KIYA
from app.controllers.ipc_bns_generate import generate_and_save_charges

router = APIRouter(prefix="/review", tags=["Review"])

@router.post("/analyze-charges", response_model=ChargeAnalysisResponse)
async def api_analyze_case_charges(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # 1. 🧠 Fat Controller Call: AI, Kanoon, aur DB teeno ek line mein handle!
        ipc_list, bns_list, precedents = await generate_and_save_charges(
            session=session,
            case_id=request.case_id,
            approved_summary=request.lawyer_approved_summary
        )

        # 2. 🌐 Frontend Response
        return ChargeAnalysisResponse(
            message="Charges and Reference Cases analyzed successfully.",
            ipc_sections=ipc_list,
            bns_sections=bns_list,
            reference_cases=precedents
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        session.rollback() 
        raise HTTPException(status_code=400, detail=f"Analysis Error: {str(e)}")
    
    