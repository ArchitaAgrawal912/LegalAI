from fastapi import APIRouter
from app.controllers.user_controller import get_users

router = APIRouter(prefix="/users", tags=["Users"])
#the router thing defines ki aage jitne bhi route hasi  voh shuru /user se ho re h 

@router.get("/")
async def users():
    return await get_users()


def test(x:int,y:int):
    return x+y