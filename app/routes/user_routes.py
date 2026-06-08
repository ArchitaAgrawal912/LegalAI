from fastapi import APIRouter
from app.operation_db.user_operation import get_users

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def users():
    return await get_users()