from sqlmodel import Session

def save_and_refresh(session: Session, db_obj):
    """Naye object ko save aur refresh karne ka engine"""
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def apply_updates_and_save(session: Session, db_obj, updates_dict: dict):
    """Purane object mein naya data overwrite karke save karne ka engine"""
    for key, value in updates_dict.items():
        setattr(db_obj, key, value)
    return save_and_refresh(session, db_obj)

def delete_and_commit(session: Session, db_obj) -> bool:
    """Kisi bhi object ko DB se udane ka engine"""
    session.delete(db_obj)
    session.commit()
    return True