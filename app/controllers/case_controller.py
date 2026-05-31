from sqlmodel import Session, select
from uuid import UUID
from app.models.case_model import Case
from app.controllers.base_controller import create, delete

# 1.>>>>>>>>>>> CREATE >>>>>>>>>>>>>
def create_case(session: Session, data: dict) -> Case:
    case = Case(**data)
    return create(session, case)


# 2. >>>>>>>>>>>>> GET >>>>>>>>>>>>
def get_case(session: Session, id: UUID) -> Case:
    query = select(Case).where(Case.id == id)
    case = session.exec(query).first()
    if case is None:
        return None
    return case


# 3. >>>>>>>>>>>>>> UPDATE >>>>>>>>>>>>>
def update_case(session: Session, id: UUID, data: dict) -> Case:
    case = get_case(session, id)
    if case is None:
        return None
    
    for key, value in data.items():
        setattr(case, key, value)
    return create(session, case)


# 4. >>>>>>>>>>>>>> DELETE >>>>>>>>>>>>>>
def delete_case(session: Session, id: UUID) -> Case:
    case = get_case(session, id)
    if case is None:
        return None
    
    return delete(session, case)