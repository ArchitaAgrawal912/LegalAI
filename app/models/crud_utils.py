from sqlmodel import Session, select, SQLModel or_
from typing import TypeVar, Type
from datetime import datetime, timezone  # 🎯 MISSING IMPORTS ADDED

# Placeholder type (SQLModel se bind kar diya for better autocomplete)
T = TypeVar("T", bound=SQLModel)
#  when  our fn is returning any 
# 🎯 NAAM THEEK KIYA: get_user_by_filters -> get_object_by_filters

def get_object_by_filters(session: Session, model: Type[T], filters: dict) -> T | None:
    """Universal engine: Ek single record laane ke liye (is_deleted check ke sath)"""
    # Forcefully soft-delete check add kar diya
    filters["is_deleted"] = False
    
    # filter_by(**filters) dictionary ke keys ko column names me convert kar deta hai
    statement = select(model).filter_by(**filters)
    return session.exec(statement).first()










# 🎯 NAAM THEEK KIYA: get_all_users_by_filters -> get_all_objects_by_filters
def get_all_objects_by_filters(
    session: Session, 
    model: Type[T], 
    filters: dict = None, 
    search_keyword: str = None,        # 🎯 Naya: Dhoondhne wala word
    search_columns: list[str] = None,  # 🎯 Naya: Kin columns me dhoondhna hai
    offset: int = 0, 
    limit: int = 10
) -> list[T]:
    """Universal engine: Pagination, Exact Filters aur Keyword Search ke sath"""
    if filters is None:
        filters = {}
        
    filters["is_deleted"] = False
    
    # 1. Exact Filters apply karo (jaise user_id, status)
    statement = select(model).filter_by(**filters)
    
    # 2. 🔥 KEYWORD SEARCH LOGIC (Universal)
    if search_keyword and search_columns:
        search_conditions = []
        for col_name in search_columns:
            # Model se dynamically column uthao (jaise LegalCase.title)
            column = getattr(model, col_name, None)
            if column is not None:
                # ILIKE case-insensitive search karta hai. "%word%" means word kahin bhi ho.
                # ilike is ki FRAUD likho ya fraud dono accepted
                search_conditions.append(column.ilike(f"%{search_keyword}%"))
        
        # Agar conditions hain, toh statement me OR lagakar add kar do
        if search_conditions:
            statement = statement.where(or_(*search_conditions))
    
    # 3. Pagination lagao
    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()
    # exec convert  stament ko sql query me and send it to supabase ka server
    # .all() ka kaam hai us raw data ko pakadna,from supabase, 
    # aur tere Python ke LegalCase Model ki ek ekdum saaf-suthri List [] banakar tujhe de dena.





# 🎯 TYPE HINTS ADDED HERE
def save_and_refresh(session: Session, db_obj: T) -> T:
    """Naye object ko save aur refresh karne ka engine"""
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj





# 🎯 TYPE HINTS ADDED HERE
def apply_updates_and_save(session: Session, db_obj: T, updates_dict: dict) -> T:
    """Purane object mein naya data overwrite karke save karne ka engine"""
    for key, value in updates_dict.items():
        setattr(db_obj, key, value)
    return save_and_refresh(session, db_obj)







# 🎯 TYPE HINTS & RETURN ADDED HERE
def delete_and_commit(session: Session, db_obj: T) -> bool:
    """Kisi bhi object ko DB se udane ka engine"""

    delete_dict = {
        "deleted_at": datetime.now(timezone.utc),
        "is_deleted": True
    }

    apply_updates_and_save(session, db_obj, delete_dict)
    return True  # 🎯 Yeh return zaroori tha bool ke liye










# bound=SQLModel??
# ans
# "Bhai T mein tu LegalCase daal, User daal, IPC daal, sab chalega. 
# Par shart yeh hai ki woh SQLModel hona chahiye (yani database ki table honi chahiye)


#     def get_all_objects(model: Type[T]) -> list[T]:
# Jab tune pass kiya model=LegalCase.

# Python bola: Achha, is baar T = LegalCase hai!

# Toh function ban gaya: def get_all_objects(model: LegalCase) -> list[LegalCase]:

# Ab VS Code ko pata chal gaya ki list ke andar LegalCase bhara hua hai. Jaise hi tu dot (.) lagayega, VS Code turant title, description, user_id sab dikha dega!