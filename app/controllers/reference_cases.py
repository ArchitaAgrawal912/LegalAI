import uuid
from sqlmodel import Session, select
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection
from app.core.case_search import fetch_reference_precedents
from app.models.crud import save_reference_cases_to_db

async def generate_and_save_references(session: Session, case_id: uuid.UUID):
    """
    Improved Controller: Fetches approved sections from DB,
    then uses them to query legal precedents.
    """
    
    # 1. 🔍 Fetch Approved Sections from DB instead of using Summary
    case = session.get(LegalCase, case_id)
    if not case:
        raise Exception("Case not found")

    # Sirf wahi sections uthao jo lawyer ne approve kiye hain
    approved_sections = [
        s for s in case.sections if s.is_approved is True
    ]
    
    if not approved_sections:
        return [] # Ya tum raise Exception kar sakte ho

    # 2. 📝 Prepare search query from Sections (IPC/BNS)
    # Hum IPC aur BNS ka combined list bana rahe hain
    search_query = " ".join([f"{s.ipc_section} {s.bns_section}" for s in approved_sections])

    # 3. 📡 Call Core Service (Kanoon search with sections)
    raw_precedents = await fetch_reference_precedents(search_query)

    # 4. 🗄️ Save to DB
    if raw_precedents:
        save_reference_cases_to_db(
            session=session, 
            case_id=case_id, 
            reference_cases_list=raw_precedents
        )
        
    return raw_precedents