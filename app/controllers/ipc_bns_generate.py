import json
import uuid
from sqlmodel import Session
from google import genai

from app.config.ai_config import get_gemini_api_key, GEMINI_MODEL
from app.prompts.legal_prompts import format_judge_prompt

# 🎯 NAYE IMPORTS: Kanoon aur DB ko yahin bula liya
from app.core.case_search import fetch_reference_precedents
from app.models.crud import save_analyzed_charges_to_db

async def generate_and_save_charges(session: Session, case_id: uuid.UUID, approved_summary: str):
    """
    Orchestrates LLM generation, Kanoon precedents fetching, 
    and saves everything to the database.
    """
    # 1. 🤖 LLM CALL (IPC/BNS nikalna)
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        raise Exception("Gemini API Key missing")
        
    ai_client = genai.Client(api_key=gemini_key)
    prompt_content = format_judge_prompt(approved_summary)
    
    response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_content
    )
    
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
    llm_data = json.loads(raw_text)
    
    ipc_list = llm_data.get("ipc_sections", [])
    bns_list = llm_data.get("bns_sections", [])

    # 2. 📡 INDIAN KANOON CALL (AWAIT lagana zaroori hai)
    raw_precedents = await fetch_reference_precedents(approved_summary)

    # 3. 🗄️ DATABASE CALL (Seedha CRUD mein bhej diya)
    save_analyzed_charges_to_db(
        session=session,
        case_id=case_id,
        lawyer_summary=approved_summary,
        ipc_list=ipc_list,
        bns_list=bns_list,
        reference_cases_list=raw_precedents
    )

    # Router ko sirf woh data wapas karo jo UI ko bhejna hai
    return ipc_list, bns_list, raw_precedents