from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import json

from app.db.database import get_session
from app.serializers.ai_serializer import ChargeAnalysisRequest, ChargeAnalysisResponse
from app.controllers.ipc_bns_generate import generate_charges_from_llm
from app.models.crud import save_analyzed_charges_to_db
from app.core.case_search import fetch_reference_precedents # Tera search function

router = APIRouter(prefix="/review", tags=["Review"])

# 🎯 Route ko `async def` bana diya
@router.post("/analyze-charges", response_model=ChargeAnalysisResponse)
async def api_analyze_case_charges(
    request: ChargeAnalysisRequest, 
    session: Session = Depends(get_session)
):
    try:
        # 1. 🧠 LLM Call: IPC/BNS nikalo
        llm_data = generate_charges_from_llm(request.lawyer_approved_summary)
        ipc_list = llm_data.get("ipc_sections", [])
        bns_list = llm_data.get("bns_sections", [])

        # 2. 📡 Indian Kanoon Call: Precedents maango (AWAIT lagana zaroori hai)
        # Note: Tere Kanoon function ko return format list of dicts karna padega jisme title, summary, aur ipc_bns_applied ho
        raw_precedents = await fetch_reference_precedents(request.lawyer_approved_summary)
        
        # 3. 🗄️ Database Call: Sab kuch ek sath save karao
        save_analyzed_charges_to_db(
            session=session,
            case_id=request.case_id,
            lawyer_summary=request.lawyer_approved_summary,
            ipc_list=ipc_list,
            bns_list=bns_list,
            reference_cases_list=raw_precedents # 🎯 Naya data DB mein gaya
        )

        # 4. 🌐 Frontend Response
        return ChargeAnalysisResponse(
            message="Charges and Reference Cases analyzed successfully.",
            ipc_sections=ipc_list,
            bns_sections=bns_list,
            reference_cases=raw_precedents # 🎯 UI ko bheja
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        session.rollback() 
        raise HTTPException(status_code=400, detail=f"Analysis Error: {str(e)}")