from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import json

from app.db.database import get_session
from app.serializers.ai_serializer import ChargeAnalysisRequest, ChargeAnalysisResponse
from app.controllers.ipc_bns_generate import generate_charges_from_llm
from app.models.crud import save_analyzed_charges_to_db # 🎯 Naya import

# @router...
router = APIRouter(prefix="/review", tags=["Review"])
@router.post("/analyze-charges", response_model=ChargeAnalysisResponse)
def api_analyze_case_charges(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # 1. 🧠 Controller Call: LLM se data maango
        llm_data = generate_charges_from_llm(request.lawyer_approved_summary)
        
        ipc_list = llm_data.get("ipc_sections", [])
        bns_list = llm_data.get("bns_sections", [])

        # 2. 🗄️ Database Call: CRUD ko bol kar DB update karao
        save_analyzed_charges_to_db(
            session=session,
            case_id=request.case_id,
            lawyer_summary=request.lawyer_approved_summary,
            ipc_list=ipc_list,
            bns_list=bns_list
        )

        # 3. 🌐 Frontend Response: Sirf response handle karo
        return ChargeAnalysisResponse(
            message="Charges analyzed and saved successfully.",
            ipc_sections=ipc_list,
            bns_sections=bns_list
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="LLM returned invalid JSON.")
    except Exception as e:
        session.rollback() 
        raise HTTPException(status_code=400, detail=f"Charge Analysis Error: {str(e)}")