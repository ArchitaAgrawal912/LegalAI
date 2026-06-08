from __future__ import annotations
from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID


class PrecedentCaseCreate(SQLModel):
    case_id: UUID
    # title: str
    # court: str
    # year: str
    # citation: str


class PrecedentCaseResponse(SQLModel):
    id: UUID
    case_id: UUID
    title: str
    court: str
    year: str
    citation: str
    source: str

