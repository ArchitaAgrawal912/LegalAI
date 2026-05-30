import uuid
from sqlmodel import Session, select

# Models import kiye
from app.models.user import User
from app.models.legal_case import LegalCase
from app.models.legal_section import LegalSection

# 🎯 Apne banaye hue Universal DB Engine import kiye
from app.controllers.crud_utils import save_and_refresh, apply_updates_and_save, delete_and_commit

# =====================================================================
# 👤 USER CRUD
# =====================================================================
def create_user(session: Session, username: str, email: str, password_hash: str) -> User:
    new_user = User(username=username, email=email, password_hash=password_hash)
    return save_and_refresh(session, new_user)

def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    return session.get(User, user_id)

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def update_user(session: Session, user_id: uuid.UUID, **kwargs) -> User | None:
    user = get_user_by_id(session, user_id)
    if not user: return None
    return apply_updates_and_save(session, user, kwargs)

def delete_user(session: Session, user_id: uuid.UUID) -> bool:
    user = get_user_by_id(session, user_id)
    if not user: return False
    return delete_and_commit(session, user)


# =====================================================================
# 📁 CASE CRUD
# =====================================================================
def create_case(session: Session, case_number: str, title: str, created_by: uuid.UUID, description: str, status: str = "open") -> LegalCase:
    new_case = LegalCase(case_number=case_number, title=title, description=description, status=status, created_by=created_by)
    return save_and_refresh(session, new_case)

def get_case_by_id(session: Session, case_id: uuid.UUID) -> LegalCase | None:
    return session.get(LegalCase, case_id)

def get_cases_by_user(session: Session, user_id: uuid.UUID) -> list[LegalCase]:
    statement = select(LegalCase).where(LegalCase.created_by == user_id)
    return session.exec(statement).all()

def update_case(session: Session, case_id: uuid.UUID, **kwargs) -> LegalCase | None:
    case = get_case_by_id(session, case_id)
    if not case: return None
    return apply_updates_and_save(session, case, kwargs)

def delete_case(session: Session, case_id: uuid.UUID) -> bool:
    case = get_case_by_id(session, case_id)
    if not case: return False
    return delete_and_commit(session, case)


# =====================================================================
# ⚖️ IPC SECTION CRUD
# =====================================================================
def create_ips_section(session: Session, section_code: str, section_name: str, description: str, case_id: uuid.UUID, penalty: str = None) -> LegalSection:
    new_section = LegalSection(section_code=section_code, section_name=section_name, description=description, penalty=penalty, case_id=case_id)
    return save_and_refresh(session, new_section)

def get_ips_section_by_id(session: Session, section_id: uuid.UUID) -> LegalSection | None:
    return session.get(LegalSection, section_id)

def get_sections_by_case(session: Session, case_id: uuid.UUID) -> list[LegalSection]:
    statement = select(LegalSection).where(LegalSection.case_id == case_id)
    return session.exec(statement).all()

def update_ips_section(session: Session, section_id: uuid.UUID, **kwargs) -> LegalSection | None:
    section = get_ips_section_by_id(session, section_id)
    if not section: return None
    return apply_updates_and_save(session, section, kwargs)

def delete_ips_section(session: Session, section_id: uuid.UUID) -> bool:
    section = get_ips_section_by_id(session, section_id)
    if not section: return False
    return delete_and_commit(session, section)

























    
# Dynamic Update: Iska fayda yeh hai ki tujhe alag se function nahi batana padega ki "sirf title update karo" ya "sirf description".
#  Frontend se jo bhi naya field aayega (chaho toh 1 field bhejo, chaho toh 10), kwargs usko pakad lega.


    # setattr(case, key, value): Yeh loop un aayi hui nayi values ko ek-ek karke purane
    #  case object par overwrite (replace) kar deta hai, aur phir commit() usey permanently DB mein save kar deta hai.




    # session.add(new_case): Yeh ekdum Amazon ke "Add to Cart" jaisa hai. Data abhi tak Supabase mein nahi gaya hai,
    #  bas memory mein ready rakha hai.

# session.commit(): Yeh "Checkout / Pay Now" button hai. Is line par actual SQL insert command banti hai aur 
# Supabase mein jaakar row save ho jati hai.

# session.refresh(new_case): Data save hote hi DB kuch naye fields generate karta hai
#  (jaise id UUID, ya created_at timestamp). Yeh line DB se woh fresh data wapas khinch kar tere new_case object mein bhar deti hai,
#  taaki route ko poori updated details mil sakein.