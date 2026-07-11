from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session, get_kanoon_service
from app.schemas.case import CaseResponse
from app.services.kanoon_service import KanoonService
from app.controllers import fetch_and_store_precedents_controller

router = APIRouter()


@router.post(
    "/{case_id}/fetch-precedents",
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Phase 3B: Query Kanoon with approved database charges, save precedents individually",
)
async def fetch_and_store_precedents(
    case_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    kanoon_service: KanoonService = Depends(get_kanoon_service),
):
    return await fetch_and_store_precedents_controller(case_id, db, kanoon_service)


#  see i waana use this kanoon service class toh mujhe onj bnaana padegga iska now if ye 20 route me aaya toh 20 baar
#  obj bnana padega so fast api provide this depends() which directly create obj for us 
#    kanoon_service: KanoonService = Depends(get_kanoon_service), this is syntax to be used

