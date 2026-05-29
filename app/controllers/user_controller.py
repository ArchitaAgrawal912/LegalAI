import uuid
from sqlmodel import Session, select
from app.models.usertable import User

# ==========================================
# 1. CREATE (Naya data database me dalna)
# ==========================================
def create_user(session: Session, username: str, email: str, password_hash: str) -> User:
    # 1. Model ka object banao (Data abhi sirf memory me hai)
    new_user = User(username=username, email=email, password_hash=password_hash)
    
    # 2. Session ko batao ki ye naya data add karna hai
    session.add(new_user)
    
    # 3. Commit karo (Asliyat me Supabase DB me jake save hoga)
    session.commit()
    
    # 4. Refresh karo (Taaki database se nayi UUID aur created_at fetch ho jaye)
    session.refresh(new_user)
    
    return new_user

# ==========================================
# 2. READ (Data fetch karna)
# ==========================================
def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    # Primary key se direct fetch karne ka sabse fast tareeqa
    return session.get(User, user_id)

def get_user_by_email(session: Session, email: str) -> User | None:
    # Custom condition (WHERE clause) lagakar fetch karna
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

# ==========================================
# 3. UPDATE (Purana data modify karna)
# ==========================================
def update_user(session: Session, user_id: uuid.UUID, **kwargs) -> User | None:
    # 1. Pehle user ko dhundo
    user = session.get(User, user_id)
    if not user:
        return None # Agar user nahi mila toh None return kar do
    
    # 2. Jo bhi naye data fields aaye hain, unhe update karo
    for key, value in kwargs.items():
        setattr(user, key, value)
        
    # 3. Wapas add aur commit karo
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

# ==========================================
# 4. DELETE (Data udana)
# ==========================================
def delete_user(session: Session, user_id: uuid.UUID) -> bool:
    # 1. Pehle user ko dhundo
    user = session.get(User, user_id)
    if not user:
        return False # User nahi hai toh False
        
    # 2. Session ko bolo isey delete karne
    session.delete(user)
    
    # 3. Commit karo (Database se hamesha ke liye saaf)
    session.commit()
    
    return True