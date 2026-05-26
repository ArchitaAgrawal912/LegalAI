from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
#we use a library called SQLAlchemy. It acts as a translator: you write normal Python code, 
# and it automatically translates it into strict PostgreSQL commands.

# 1. The Master Blueprint (The Empty Filing Cabinet)
class Base(DeclarativeBase):
    pass

# 2. Drawer #1: The Users Table
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    
    # We call it 'hashed_password' to remind ourselves NEVER to save plain text passwords
    hashed_password: Mapped[str] = mapped_column(String(255)) 
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    
    # A link to the Cases table: "Show me all cases created by this user"
    cases: Mapped[List["Case"]] = relationship(back_populates="owner")


# 3. Drawer #2: The Cases Table
class Case(Base):
    __tablename__ = "cases"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    case_description: Mapped[str] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending") # "accepted", "rejected", etc.
    
    # Auto-generates the exact timestamp when this row is created
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # We can store the whole list of Kanoon cases here as a JSON object
    precedent_cases: Mapped[Optional[dict]] = mapped_column(JSON) 
    
    # The Foreign Key linking this case to a specific User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="cases")
    
    # A link to the IPC Sections table: "Show me all charges for this case"
    ipc_sections: Mapped[List["IpcSection"]] = relationship(back_populates="parent_case")


# 4. Drawer #3: The IPC Sections Table
class IpcSection(Base):
    __tablename__ = "ipc_sections"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    ipc_section: Mapped[str] = mapped_column(String(50))
    bns_equivalent: Mapped[str] = mapped_column(String(50))
    offense: Mapped[str] = mapped_column(String(255))
    explanation: Mapped[str] = mapped_column(Text)
    
    # THE FOREIGN KEY: This staples this specific charge directly to a Case ID
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    parent_case: Mapped["Case"] = relationship(back_populates="ipc_sections")