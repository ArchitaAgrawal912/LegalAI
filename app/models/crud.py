import uuid
from sqlmodel import Session, select, or_

# Models import kiye
from app.models.user import User
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection
from app.models.reference_cases import ReferenceCase
# 🎯 Universal DB Engines import kiye
from app.models.crud_utils import (
    save_and_refresh, 
    apply_updates_and_save, 
    delete_and_commit,
    get_object_by_filters,       # <-- Naya get engine
    get_all_objects_by_filters   # <-- Naya get list engine
)

# =====================================================================
# 👤 USER CRUD
# =====================================================================
def create_user(session: Session, name: str, email: str, password_hash: str, phone_no: str | None = None) -> User:
    new_user = User(name=name, email=email, password_hash=password_hash, phone_no=phone_no)
    return save_and_refresh(session, new_user)

def get_object_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    # 🎯 Ab direct dictionary pass ho rahi hai
    return get_object_by_filters(session, User, {"id": user_id})

def get_user_by_email(session: Session, email: str) -> User | None:
    return get_object_by_filters(session, User, {"email": email})

def update_user(session: Session, user_id: uuid.UUID, **kwargs) -> User | None:
    user = get_object_by_id(session, user_id)
    if not user: return None
    return apply_updates_and_save(session, user, kwargs)

def delete_user(session: Session, user_id: uuid.UUID) -> bool:

    user = get_object_by_id(session, user_id) 
    if not user:
        return False
    
    # 1. Pehle us user ke saare cases nikal lo
    user_cases = get_cases_by_user(session, user_id, limit=1000) # limit high rakho
    
    # 2. Har case ke liye wahi delete_case logic chalao
    for case in user_cases:
        delete_case(session, case.id)
        
    # 3. Last mein User khud delete karo
    return delete_and_commit(session, user)

# =====================================================================
# 📁 CASE CRUD
# =====================================================================
def create_case(session: Session, title: str, user_id: uuid.UUID, raw_description: str, status: str = "pending") -> LegalCase:
    new_case = LegalCase(title=title, raw_description=raw_description, status=status, user_id=user_id)
    return save_and_refresh(session, new_case)

def get_case_by_id(session: Session, case_id: uuid.UUID) -> LegalCase | None:
    return get_object_by_filters(session, LegalCase, {"id": case_id})

def get_cases_by_user(session: Session, user_id: uuid.UUID, offset: int = 0, limit: int = 10) -> list[LegalCase]:
    # 🎯 Universal engine ko pagination parameters pass kar diye
    return get_all_objects_by_filters(session, LegalCase, {"user_id": user_id}, offset=offset, limit=limit)

def update_case(session: Session, case_id: uuid.UUID, **kwargs) -> LegalCase | None:
    case = get_case_by_id(session, case_id)
    if not case: return None
    return apply_updates_and_save(session, case, kwargs)
# app/models/crud.py

def delete_case(session: Session, case_id: uuid.UUID) -> bool:
    """Case delete karo aur uske saare sections & references bhi soft delete karo."""
    case = get_case_by_id(session, case_id)
    if not case:
        return False
    
    # 1. Saare Sections soft delete karo
    sections = get_sections_by_case(session, case_id)
    for section in sections:
        delete_and_commit(session, section)
        
    # 2. Saare Reference Cases soft delete karo
    delete_all_references_for_case(session, case_id)
    
    # 3. Main Case delete karo
    return delete_and_commit(session, case)

# =====================================================================
# ⚖️ LEGAL SECTION CRUD
# =====================================================================
def create_legal_section(session: Session, ipc_section: str, bns_section: str, reason: str, case_id: uuid.UUID) -> LegalSection:
    new_section = LegalSection(ipc_section=ipc_section, bns_section=bns_section, reason=reason, case_id=case_id)
    return save_and_refresh(session, new_section)

def get_section_by_id(session: Session, section_id: uuid.UUID) -> LegalSection | None:
    return get_object_by_filters(session, LegalSection, {"id": section_id})

def get_sections_by_case(session: Session, case_id: uuid.UUID) -> list[LegalSection]:
    return get_all_objects_by_filters(session, LegalSection, {"case_id": case_id})

def update_legal_section(session: Session, section_id: uuid.UUID, **kwargs) -> LegalSection | None:
    section = get_section_by_id(session, section_id)
    if not section: return None
    return apply_updates_and_save(session, section, kwargs)

def delete_legal_section(session: Session, section_id: uuid.UUID) -> bool:
    section = get_section_by_id(session, section_id)
    if not section: return False
    return delete_and_commit(session, section)




# =====================================================================
# 📚 REFERENCE CASE CRUD
# =====================================================================
from app.models.reference_cases import ReferenceCase

def get_reference_by_id(session: Session, ref_id: uuid.UUID) -> ReferenceCase | None:
    """Ek specific reference case laane ke liye."""
    # Tera universal engine automatically is_deleted=False handle kar lega!
    return get_object_by_filters(session, ReferenceCase, {"id": ref_id})

def get_references_by_case(session: Session, case_id: uuid.UUID, offset: int = 0, limit: int = 10) -> list[ReferenceCase]:
    """Ek case ke saare active reference cases laane ke liye."""
    return get_all_objects_by_filters(
        session, 
        ReferenceCase, 
        {"case_id": case_id}, 
        offset=offset, 
        limit=limit
    )

def update_reference(session: Session, ref_id: uuid.UUID, **kwargs) -> ReferenceCase | None:
    """Agar admin/lawyer AI generated title ya summary ko edit karna chahe."""
    ref = get_reference_by_id(session, ref_id)
    if not ref: 
        return None
    return apply_updates_and_save(session, ref, kwargs)

def delete_reference(session: Session, ref_id: uuid.UUID) -> bool:
    """Single reference case ko soft delete karne ke liye."""
    ref = get_reference_by_id(session, ref_id)
    if not ref: 
        return False
    # Tera universal engine isko automatically is_deleted = True kar dega!
    return delete_and_commit(session, ref)


def delete_all_references_for_case(session: Session, case_id: uuid.UUID) -> bool:
    """Ek main LegalCase delete hone par uske saare reference cases ko soft delete karega."""
    
    # 1. Pehle us case id wale saare active references nikal lo
    references = get_references_by_case(session, case_id)
    
    # 2. Loop chala kar ek-ek karke sabko delete(soft) kar do
    for ref in references:
        delete_and_commit(session, ref)
        
    return True













# =====================================================================
# 🧠 AI & CUSTOM BUSINESS LOGIC CRUD
# =====================================================================
def search_cases(
    session: Session, 
    user_id: uuid.UUID = None, 
    keyword: str = None, 
    offset: int = 0, 
    limit: int = 10
) -> list[LegalCase]:
    
    filters = {}
    # Agar user_id di hai, toh sirf uske cases me search karega
    if user_id:
        filters["user_id"] = user_id
        
    # 🎯 Universal Engine ko batao ki title aur raw_description me search karna hai
    return get_all_objects_by_filters(
        session=session, 
        model=LegalCase, 
        filters=filters,
        search_keyword=keyword,
        search_columns=["title", "raw_description"], # Yahan column ke naam pass kiye
        offset=offset, 
        limit=limit
    )



def create_case_with_summary(
    session: Session, 
    user_id: uuid.UUID, 
    raw_description: str, 
    title: str, 
    llm_summary: str
) -> LegalCase:
    """Creates a new Legal Case using the utility engine."""
    
    new_case = LegalCase(
        user_id=user_id,
        title=title,
        raw_description=raw_description,
        llm_summary=llm_summary
    )
    
    # 🎯 Seedha tera utility function call kiya!
    return save_and_refresh(session, new_case)

from app.models.crud_utils import save_and_refresh # (Yeh upar imported hona chahiye)

def update_section_approval(
    session: Session,
    section_id: uuid.UUID,
    is_approved: bool,
    rejection_reason: str | None = None
):
    """Updates the approval status of a single generated Legal Section."""
    try:
        # 1. Database se section nikalo
        section = session.get(LegalSection, section_id)
        if not section:
            raise ValueError("Legal Section not found")

        # 2. Values update karo
        section.is_approved = is_approved
        section.rejection_reason = rejection_reason

        # 3. 🎯 Tera Utility Engine Call
        return save_and_refresh(session, section)
        
    except Exception as e:
        session.rollback()
        raise e



def save_ipc_bns_to_db(session: Session, case_id: uuid.UUID, lawyer_summary: str, ipc_list: list, bns_list: list):
    """Saves ONLY the generated IPC and BNS sections to the database."""
    
    db_case = session.get(LegalCase, case_id)
    if not db_case:
        raise ValueError("Case not found")

    # Update case status
    db_case.lawyer_approved_summary = lawyer_summary
    db_case.status = "inprogress"
    session.add(db_case)

    # Save IPC Sections
    for item in ipc_list:
        new_section = LegalSection(
            case_id=db_case.id,
            ipc_section=item.get("section", ""),
            bns_section="N/A", 
            title=item.get("title", "Unknown offence"),
            probability=float(item.get("probability", 0.0)),
            reason=item.get("reason", ""),
            source="LLM"
        )
        session.add(new_section)

    # Save BNS Sections
    for item in bns_list:
        new_section = LegalSection(
            case_id=db_case.id,
            ipc_section="N/A",
            bns_section=item.get("section", ""),
            title=item.get("title", "Unknown offence"),
            probability=float(item.get("probability", 0.0)),
            reason=item.get("reason", ""),
            source="LLM"
        )
        session.add(new_section)

    session.commit()
    return db_case




def save_reference_cases_to_db(
    session: Session, 
    case_id: uuid.UUID, 
    reference_cases_list: list
):
    """Saves ONLY the Indian Kanoon reference cases to the database."""
    
    # Agar list khali hai toh faaltu DB commit mat karo
    if not reference_cases_list:
        return False 

    for ref in reference_cases_list:
        new_ref = ReferenceCase(
            case_id=case_id,
            title=ref.get("title", "Unknown"),
            summary=ref.get("summary", ""),
            ipc_bns_applied=ref.get("ipc_bns_applied", "Not specified"),
            is_deleted=False  # Humne model mein column add kar diya hai, toh yeh safely chalega
        )
        session.add(new_ref)

    session.commit()
    return True

   