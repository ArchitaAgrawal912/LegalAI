from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, ForeignKey

class CaseIPCLink(SQLModel, table=True):
    __tablename__ = "caseipclink"

    case_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("case.id"), primary_key=True)
    )
    ipc_id: Optional[int] = Field(
        sa_column=Column(Integer, ForeignKey("ipcsection.id"), primary_key=True)
    )