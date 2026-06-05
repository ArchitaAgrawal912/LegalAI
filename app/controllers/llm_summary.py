# app/controllers/llm_summary.py

import uuid
from sqlmodel import Session
from google import genai

from app.config.ai_config import get_gemini_api_key, GEMINI_MODEL

# 🎯 NAYE IMPORTS: Dono naye prompts ko bula liya
from app.prompts.llm_summary import format_summary_prompt, format_title_prompt
from app.models.crud import create_case_with_summary 

def generate_summary_and_save(session: Session, user_id: uuid.UUID, raw_description: str):
    """
    Takes raw text, makes 2 separate Gemini calls for Title and Summary, 
    and saves the complete case directly to the Database.
    """
    
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        raise Exception("Gemini API Key missing")
        
    ai_client = genai.Client(api_key=gemini_key)
    
    # --------------------------------------------------
    # 🤖 CALL 1: Generate ONLY Summary
    # --------------------------------------------------
    summary_prompt = format_summary_prompt(raw_description)
    summary_response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=summary_prompt
    )
    llm_summary = summary_response.text.strip()
    
    # --------------------------------------------------
    # 🤖 CALL 2: Generate ONLY Title
    # --------------------------------------------------
    title_prompt = format_title_prompt(raw_description)
    title_response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=title_prompt
    )
    title = title_response.text.strip()
    
    # 🗄️ DATABASE CALL (Dono values milne ke baad DB bhej do)
    new_case = create_case_with_summary(
        session=session,
        user_id=user_id,
        raw_description=raw_description,
        title=title,
        llm_summary=llm_summary
    )
    
    return new_case