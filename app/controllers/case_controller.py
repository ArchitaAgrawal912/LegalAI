import uuid
from sqlmodel import Session, select
from app.models.casetable import Case

# ==========================================
# 1. CREATE
# ==========================================
def create_case(session: Session, case_number: str, title: str, created_by: uuid.UUID, description: str = None, status: str = "open") -> Case:
    new_case = Case(
        case_number=case_number, 
        title=title, 
        description=description, 
        status=status, 
        created_by=created_by
    )
    session.add(new_case)
    session.commit()
    session.refresh(new_case)
    return new_case

# ==========================================
# 2. READ
# ==========================================
def get_case_by_id(session: Session, case_id: uuid.UUID) -> Case | None:
    return session.get(Case, case_id)

def get_cases_by_user(session: Session, user_id: uuid.UUID) -> list[Case]:
    # Ek user ke saare cases nikalne ke liye
    statement = select(Case).where(Case.created_by == user_id)
    return session.exec(statement).all()

# ==========================================
# 3. UPDATE
# ==========================================
def update_case(session: Session, case_id: uuid.UUID, **kwargs) -> Case | None:
    case = session.get(Case, case_id)
    if not case:
        return None
    
    for key, value in kwargs.items():
        setattr(case, key, value)
        
    session.add(case)
    session.commit()
    session.refresh(case)
    return case

# ==========================================
# 4. DELETE
# ==========================================
def delete_case(session: Session, case_id: uuid.UUID) -> bool:
    case = session.get(Case, case_id)
    if not case:
        return False
        
    session.delete(case)
    session.commit()
    return True



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