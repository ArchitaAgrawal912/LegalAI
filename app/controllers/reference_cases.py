# app/controllers/reference_cases.py

import uuid
from sqlmodel import Session

# 🎯 Service aur CRUD imports
from app.core.case_search import fetch_reference_precedents
from app.models.crud import save_reference_cases_to_db

async def generate_and_save_references(session: Session, case_id: uuid.UUID, approved_summary: str):
    """
    Super Simple Controller: Fetches data from core service 
    and commits directly to the Reference table.
    """
    
    # 1. 📡 Call Core Service (Kanoon + LLM processing sab iske andar ho jayega)
    raw_precedents = await fetch_reference_precedents(approved_summary)

    # 2. 🗄️ Database Call (Sirf tabhi chalega jab actual data aayega)
    if raw_precedents:
        save_reference_cases_to_db(
            session=session, 
            case_id=case_id, 
            reference_cases_list=raw_precedents
        )
        
    # 3. Return clean data for Router response
    return raw_precedents