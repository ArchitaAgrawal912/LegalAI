from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.schemas.case import CaseRead
from app.controllers import get_user_cases_controller

router = APIRouter()


@router.get(
    "/",
    response_model=List[CaseRead],
    status_code=status.HTTP_200_OK,
    summary="Fetch all cases for a specific user",
)
async def get_user_cases(
    user_id: UUID,
    search: str | None = Query(None, description="Search by case title or description"),
    skip: int = Query(0, ge=0, description="How many records to skip"),
    limit: int = Query(100, ge=1, le=100, description="How many records to return"),
    db: AsyncSession = Depends(get_db_session),
):
    return await get_user_cases_controller(user_id, search, skip, limit, db)


#  search bar me  ya toh kuch user seacrh kareag aagr user ne 
#  kuch nhi dalaand search bda dia toh None jayega vha
# desscription bas swagger k liye hai
# if we have 5 cases and we set skip = 2 toh first 2 skip h
# jayege and baaki 3 aayege
# ge=2  mean skip value should be >=0
# Database me

# 1000  matched cases hai 

# Tum bolte ho

# limit=10

# To sirf

# 10 shuru vale matched cases will come

# records milenge.
#  by default limit=100  lgai hai aur max limit=100 hai