from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from app.serializers.precedent_serializer import PrecedentCaseResponse

from app.core.database import get_db
from app.operation_db.precedent_operation import(
    get_precedents_by_case, 
    delete_precedent
)
from app.serializers.common_response import APIResponse

router = APIRouter(prefix="/precedents", tags=["Precedent Cases"])

@router.get("/case/{case_id}", response_model=APIResponse)
def get_precedents_route(case_id: UUID, session: Session = Depends(get_db)):
    precedents = get_precedents_by_case(session, case_id)

    return APIResponse(
    success=True,
    message="Precedents fetched successfully",
    data=precedents
)


@router.delete("/{precedent_id}", response_model=PrecedentCaseResponse)
def delete_precedent_route(precedent_id: UUID, session: Session = Depends(get_db)):
    precedent = delete_precedent(session, precedent_id)

    if precedent is None:
        raise HTTPException(
            status_code=404,
            detail="Precedent not found"
        )

    return precedent