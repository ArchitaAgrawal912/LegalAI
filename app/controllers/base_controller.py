from sqlmodel import Session, SQLModel

def create(session: Session, obj: SQLModel) -> SQLModel:
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete(session: Session, obj: SQLModel) -> SQLModel:
    session.delete(obj)
    session.commit()
    return obj