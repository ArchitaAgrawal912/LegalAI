from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid
from typing import List
# Tumhara DB session aur controllers
from app.db.database import get_session
from app.controllers.user_controller import create_user, get_user_by_id

# Tumhare banaye hue serializers
from app.serializers.user_serializer import UserCreate, UserResponse

# Router initialize kiya (Tags se Swagger UI me mast grouping hoti hai)
router = APIRouter(prefix="/users", tags=["Users"])

# ==========================================
# 1. CREATE USER ROUTE (POST)
# ==========================================
# 🎯 Magic Trick: response_model=UserResponse likhne se FastAPI khud 
# password filter kar dega aur sirf safe data return karega!
@router.post("/bulk", response_model=List[UserResponse])
def api_create_multiple_users(users_data: List[UserCreate], session: Session = Depends(get_session)):
    try:
        created_users = []
        # Frontend se jo list aayi, uspar loop lagaya
        for data in users_data:
            user = create_user(
                session=session,
                username=data.username,
                email=data.email,
                password_hash=data.password
            )
            created_users.append(user)
        return created_users
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bulk User Error: {str(e)}")

# ==========================================
# 2. GET USER ROUTE (GET)
# ==========================================
@router.get("/{user_id}", response_model=UserResponse)
def api_get_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User nahi mila bhai!")
    return user