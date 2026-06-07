import json
import uuid
from sqlmodel import Session
from app.core.ai_service import call_gemini_llm
from app.prompts.legal_prompts import format_judge_prompt
from app.models.crud import save_ipc_bns_to_db

def generate_and_save_ipc_bns(session: Session, case_id: uuid.UUID, approved_summary: str):
    """
    Calls Gemini with a 3-attempt retry policy and provides a safe fallback if AI fails.
    """
    # 1. Prompt Taiyaar Karo
    prompt_content = format_judge_prompt(approved_summary)
    
    # 2. ⚡ AI Service Call (With tenacity retries inside)
    try:
        # Agar ye 3 baar mein bhi fail hua, toh Exception raise karega
        clean_text = call_gemini_llm(prompt_content)
        llm_data = json.loads(clean_text)
        
    except Exception as e:
        # 3. 🛡️ FALLBACK MECHANISM
        # Agar AI service 3 attempt ke baad bhi down hai, toh hum app ko crash nahi hone denge
        print(f"❌ Critical Error: AI Service failed after 3 retries: {e}")
        
        # Hum empty data ke saath proceed karenge ya custom error flag set karenge
        llm_data = {"ipc_sections": [], "bns_sections": []}
        
    # 4. Data Extraction
    ipc_list = llm_data.get("ipc_sections", [])
    bns_list = llm_data.get("bns_sections", [])

    # 5. DATABASE CALL
    # Agar AI fail hua, toh empty list save ho jayegi (or handle accordingly)
    save_ipc_bns_to_db(
        session=session,
        case_id=case_id,
        lawyer_summary=approved_summary,
        ipc_list=ipc_list,
        bns_list=bns_list
    )

    return ipc_list, bns_list