from sqlmodel import Session, select
from app.models.user_model import User
from uuid import UUID
from app.operation_db.base_controller import create, soft_delete, update_and_change

def create_user(session: Session, data: dict) -> User: # actual data received from user
    user = User(**data) # unpacking dictionary
    return create(session, user)
# user object is created

# def create_user(...) -> User =====> means User object RETURN hoga 

# name(left side) ===> column ka naam
# name(rt side) ===> actual value from function parameter

# Controller ==> logic defining
# Router ==> request receive krna, controller ko call krna


def get_user(session: Session, id: UUID) -> User:
    query = select(User).where(User.id == id, User.is_deleted == False) # see another condition also
    user = session.exec(query).first()
    return user

# select( ) query banata hai Python me
# session.exec() query database me bhejta hai -> result laata hai
# .first() -> single row / object

def update_user(session: Session, id: UUID, data: dict) -> User: 
    user = get_user(session, id) # 1.search

    if user is None:
        return None # no user found
    return update_and_change(session, user, data)

    # setattr(user, key, value) ==> dynamically kisi bhi field set karo.

    # session.add(user)
    # session.commit()
    # session.refresh(user) ===> replaced by -> create()


def delete_user(session: Session, id: UUID) -> bool:
    user = get_user(session, id) # Search the user
    if user is None:
        return None
    
    return soft_delete(session, user)


    # session.delete(user)
    # session.commit() ===> replaced by -> delete()