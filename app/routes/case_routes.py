from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from uuid import UUID
from typing import Optional
from app.core.database import get_db
from app.operation_db.case_controller import (
    create_case,
    get_case,
    get_all_cases,
    update_case,
    delete_case,
    generate_and_save_summary,
    approve_summary,
    reject_summary
)
from app.serializers.case_serializer import (
    CaseCreate,
    CaseResponse,
    CaseUpdate,
    SummaryResponse,
    ApproveRejectRequest
)

router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)

@router.post("/", response_model=CaseResponse)
def create_case_route(payload: CaseCreate, session: Session = Depends(get_db)):
    case = create_case(session, payload.model_dump())
    return case

@router.get("/{case_id}", response_model=CaseResponse)
def get_case_route(case_id: UUID, session: Session = Depends(get_db)):
    case = get_case(session, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.get("/user/{user_id}", response_model=list[CaseResponse])
def get_all_cases_route(user_id: UUID, search: Optional[str] = None, page: int = 1, limit: int = 10, session: Session = Depends(get_db)):
    return get_all_cases(session, user_id, search, page, limit)


@router.patch("/{case_id}", response_model=CaseResponse)
def update_case_route(case_id: UUID, payload: CaseUpdate, session: Session = Depends(get_db)):
    case = update_case(session, case_id,payload.model_dump(exclude_unset=True))
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.delete("/{case_id}", response_model=CaseResponse)
def delete_case_route(case_id: UUID, session: Session = Depends(get_db)):
    case = delete_case(session, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


# LLM Summary generate 
@router.post("/{case_id}/generate-summary", response_model=SummaryResponse)
def generate_summary_route(case_id: UUID, session: Session = Depends(get_db)):
    case = generate_and_save_summary(session, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

# Approve summary
@router.patch("/{case_id}/approve-summary", response_model=CaseResponse)
def approve_summary_route(case_id: UUID, session: Session = Depends(get_db)):
    case = approve_summary(session, case_id)
    if case is None:
        raise HTTPException(status_code=404,detail="Case not found")
    return case

# Reject summary
@router.patch("/{case_id}/reject-summary", response_model=CaseResponse)
def reject_summary_route(case_id: UUID, session: Session = Depends(get_db)):
    case = reject_summary(session, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

    