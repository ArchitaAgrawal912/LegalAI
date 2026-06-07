# app/controllers/llm_summary.py

import json
import uuid
from sqlmodel import Session

# 🎯 NAYA IMPORT: Tera Universal AI Engine
from app.core.ai_service import call_gemini_llm 
from app.prompts.llm_summary import format_combined_prompt
from app.models.crud import create_case_with_summary 

# =================================================================
# 🧠 MAIN CONTROLLER
# =================================================================
def generate_summary_and_save(session: Session, user_id: uuid.UUID, raw_description: str):
    """
    Controller logic that uses the resilient Universal AI helper and saves to DB.
    """
    
    # 1. Prompt Taiyaar kiya
    prompt = format_combined_prompt(raw_description)
    
    try:
        # 2. 🤖 Call AI (Retries aur Gemini logic ab ai_service.py handle karega)
        clean_response_text = call_gemini_llm(prompt)
        
        # 3. JSON Parse kiya
        ai_data = json.loads(clean_response_text)
        title = ai_data.get("title", "Unknown vs Unknown - Legal Incident")
        llm_summary = ai_data.get("summary", raw_description)
        
    except Exception as e:
        # Agar 3 retry ke baad bhi fail ho gaya ya JSON format galat aaya
        print(f"❌ AI Failed completely after retries: {str(e)}")
        title = "Error Generating Title"
        llm_summary = raw_description

    # 4. 🗄️ DATABASE CALL 
    new_case = create_case_with_summary(
        session=session,
        user_id=user_id,
        raw_description=raw_description,
        title=title,
        llm_summary=llm_summary
    )
    
    return new_case