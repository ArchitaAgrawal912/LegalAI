# app/routers/reference_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import get_session

# 🎯 Naye Response Model aur Request ko import kiya
from app.serializers.ai_serializer import ChargeAnalysisRequest, ReferenceOnlyResponse
from app.controllers.reference_cases import generate_and_save_references

router = APIRouter(prefix="/references", tags=["Reference Cases"])

# 🎯 response_model add kar diya
@router.post("/fetch", response_model=ReferenceOnlyResponse)
async def api_fetch_case_references(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # Controller Call (Yeh await ke sath chalega kyunki Kanoon slow hai)
        precedents = await generate_and_save_references(
            session=session, 
            case_id=request.case_id, 
            approved_summary=request.lawyer_approved_summary
        )
        
        # 🎯 Pydantic Response Model return kiya
        return ReferenceOnlyResponse(
            message="Reference cases fetched successfully.",
            reference_cases=precedents
        )
        
    except Exception as e:
        session.rollback() 
        raise HTTPException(status_code=400, detail=f"Reference Fetch Error: {str(e)}")