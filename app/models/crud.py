import uuid
from sqlmodel import Session 

# Models import kiye
from app.models.user import User
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection

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
    if not user: return False
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

def delete_case(session: Session, case_id: uuid.UUID) -> bool:
    case = get_case_by_id(session, case_id)
    if not case: return False
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