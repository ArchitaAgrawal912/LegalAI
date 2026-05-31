from sqlmodel import Session, select
from uuid import UUID
from app.models.case_model import Case
from app.operation_db.base_controller import create, update_and_change, soft_delete

# 1.>>>>>>>>>>> CREATE >>>>>>>>>>>>>
def create_case(session: Session, data: dict) -> Case:
    case = Case(**data)
    return create(session, case)


# 2. >>>>>>>>>>>>> GET >>>>>>>>>>>>
def get_case(session: Session, id: UUID) -> Case:
    query = select(Case).where(Case.id == id, Case.is_deleted == False)
    case = session.exec(query).first()
    if case is None:
        return None
    return case


# 3. >>>>>>>>>>>>>> UPDATE >>>>>>>>>>>>>
def update_case(session: Session, id: UUID, data: dict) -> Case:
    case = get_case(session, id)
    if case is None:
        return None
        return update_and_change(session, case, kwargs)
    
    for key, value in data.items():
        setattr(case, key, value)
    return create(session, case)


# 4. >>>>>>>>>>>>>> DELETE >>>>>>>>>>>>>>
def delete_case(session: Session, id: UUID) -> bool:
    case = get_case(session, id)
    if case is None:
        return None
    
    return soft_delete(session, case)