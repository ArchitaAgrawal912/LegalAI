from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.controllers.auth_controller import (
    register_controller,
    login_controller,
)
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await register_controller(request, db)


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await login_controller(request, db)

# Later, when you are ready to secure the application for production, you only h
# ave to change db_user.password_hash != request.password to a secure hash checker 
# (like verify_password(request.password, db_user.password_hash)), and the frontend won't have to change a single line of code!
