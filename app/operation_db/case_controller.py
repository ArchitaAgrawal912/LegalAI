from sqlmodel import Session, select
from uuid import UUID
from app.models.case_model import Case
from app.operation_db.base_controller import create, update_and_change, soft_delete

# 1.>>>>>>>>>>> CREATE >>>>>>>>>>>>>
def create_case(session: Session, data: dict) -> Case:
    case = Case(**data)
    return create(session, case)

# (**data) -> Ye dictionary ko Case object me convert kar raha hai.

# 2. >>>>>>>>>>>>> GET >>>>>>>>>>>>
def get_case(session: Session, id: UUID) -> Case | None:
    query = select(Case).where(Case.id == id, Case.is_deleted == False)
    case = session.exec(query).first()

    return case


# 3. >>>>>>>>>>>>>> UPDATE >>>>>>>>>>>>>
def update_case(session: Session, id: UUID, data: dict) -> Case | None:
    case = get_case(session, id)
    
    return update_and_change(session, case, data)
    
    

# 4. >>>>>>>>>>>>>> DELETE >>>>>>>>>>>>>>
def delete_case(session: Session, id: UUID) -> Case | None:
    case = get_case(session, id)
    
    return soft_delete(session, case)

# 5. GET ALL CASES WITH SEARCH
def get_all_cases(session: Session, user_id: UUID, search: str = None, page: int = 1, limit: int = 10) -> list[Case]:
    query = select(Case).where(Case.user_id == user_id, Case.is_deleted == False)

    if search:
        query = query.where(
            Case.case_description.ilike(f"%{search}%") | 
            Case.title.ilike(f"%{search}%")                     
        )
    offset = (page - 1) * limit

    cases = session.exec(query.offset(offset).limit(limit)).all()
    
    return cases


# % → SQL Wildcard : Is jagah kuch bhi ho sakta hai.

# Kitna data chhodna hai? → offset
# Kitna data lena hai? → limit

# Session = Database Conversation
# Session bolta hai:
#"Main database se connected hoon."