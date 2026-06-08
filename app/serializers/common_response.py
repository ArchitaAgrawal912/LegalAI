from typing import Any
from sqlmodel import SQLModel

class APIResponse(SQLModel):
    success: bool
    message: str
    data: Any = None