from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, LoginResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


async def register_controller(
    request: UserCreate,
    db: AsyncSession,
):
    # Check email already exists
    existing_user = await crud.user.get_by_email(
        db,
        email=request.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    # Hash password
    hashed_password = hash_password(request.password)

    db_user = User(
        name=request.name,
        email=request.email,
        phone_no=request.phone_no,
        password_hash=hashed_password,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return {
        "message": "User registered successfully.",
        "user_id": db_user.id,
    }


async def login_controller(
    request: LoginRequest,
    db: AsyncSession,
) -> LoginResponse:

    db_user = await crud.user.get_by_email(
        db,
        email=request.email,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(
        request.password,
        db_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        {
            "sub": str(db_user.id)
        }
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(db_user.id),
        name=db_user.name,
        email=db_user.email,
    )