from __future__ import annotations
from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID

class CaseCreate(SQLModel):
    title: Optional[str]
    case_description: str
    user_id: UUID

class CaseUpdate(SQLModel):
    title: Optional[str] = None
    case_description: Optional[str] = None

class CaseResponse(SQLModel):
    id: UUID
    title: Optional[str] = None
    case_description: str
    llm_summary: Optional[str] = None
    status: str
    user_id: UUID

class SummaryResponse(SQLModel):
    id: UUID
    title: str
    llm_summary: str

class ReviewSummaryRequest(SQLModel):
    summary: str

class ApproveRejectRequest(SQLModel):
    approved: bool

