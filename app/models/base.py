import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

class CoreModel(SQLModel):
    # Dhyan do: Yahan table=True NAHI hai
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)