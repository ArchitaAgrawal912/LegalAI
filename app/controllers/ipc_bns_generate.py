# app/controllers/ipc_bns_generate.py

import json
import uuid
from sqlmodel import Session

# 🎯 Universal AI Caller aur Prompt
from app.core.ai_service import call_gemini_llm
from app.prompts.legal_prompts import format_judge_prompt

# 🎯 Sirf Charges save karne wala naya CRUD import
from app.models.crud import save_ipc_bns_to_db

def generate_and_save_ipc_bns(session: Session, case_id: uuid.UUID, approved_summary: str):
    """
    Calls Gemini to generate IPC/BNS sections and saves them to the DB.
    """
    
    # 1. 🤖 Prompt Taiyaar Karo
    prompt_content = format_judge_prompt(approved_summary)
    
    # 2. ⚡ Universal AI Service Call (Retries automatically handle honge)
    clean_text = call_gemini_llm(prompt_content)
    
    # 3. 🧹 JSON Data Parse Karo (With Safety Net)
    try:
        llm_data = json.loads(clean_text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing failed in IPC/BNS generation: {e}")
        # Fallback agar JSON break ho jaye
        llm_data = {"ipc_sections": [], "bns_sections": []}
    
    ipc_list = llm_data.get("ipc_sections", [])
    bns_list = llm_data.get("bns_sections", [])

    # 4. 🗄️ DATABASE CALL (Sirf specific CRUD function hit hoga)
    save_ipc_bns_to_db(
        session=session,
        case_id=case_id,
        lawyer_summary=approved_summary,
        ipc_list=ipc_list,
        bns_list=bns_list
    )

    # 5. Router ko clean data return karo
    return ipc_list, bns_list