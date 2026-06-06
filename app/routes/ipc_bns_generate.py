# app/routers/charge_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import get_session

# 🎯 Naye Response Model aur Request ko import kiya
from app.serializers.ai_serializer import ChargeAnalysisRequest, ChargeOnlyResponse
from app.controllers.ipc_bns_generate import generate_and_save_ipc_bns

router = APIRouter(prefix="/charges", tags=["Charges & Sections"])

# 🎯 response_model add kar diya taaki Swagger API ekdum clean dikhe
@router.post("/analyze", response_model=ChargeOnlyResponse)
def api_analyze_case_charges(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # Controller Call
        ipc_list, bns_list = generate_and_save_ipc_bns(
            session=session, 
            case_id=request.case_id, 
            approved_summary=request.lawyer_approved_summary
        )
        
        # 🎯 Pydantic Response Model return kiya
        return ChargeOnlyResponse(
            message="Charges extracted successfully.",
            ipc_sections=ipc_list,
            bns_sections=bns_list
        )
        
    except Exception as e:
        session.rollback() 
        raise HTTPException(status_code=400, detail=f"Charges Analysis Error: {str(e)}")
    