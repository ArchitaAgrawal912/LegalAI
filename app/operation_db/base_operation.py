from sqlmodel import Session, SQLModel
from datetime import datetime, UTC


def create(session: Session, obj: SQLModel) -> SQLModel:
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def update_and_change(session: Session, obj: SQLModel, updates_dict: dict) -> SQLModel | None:
    if obj is None:
        return None
    for key, value in updates_dict.items():
        setattr(obj, key, value)
    obj.updated_at = datetime.now(UTC)
    return create(session, obj)

def soft_delete(session: Session, obj: SQLModel) -> SQLModel | None :
    if obj is None:
        return None
    obj.is_deleted = True
    obj.updated_at = datetime.now(UTC)
    obj.deleted_at = datetime.now(UTC)
    return create(session, obj)