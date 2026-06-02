from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_db
from app.operation_db.section_controller import (
    create_section,
    get_section,
    get_sections_by_case,
    update_section,
    delete_section,
    verify_section
)

from app.serializers.section_serializer import(
    LegalSectionCreate,
    LegalSectionUpdate,
    LegalSectionResponse
)

router = APIRouter(prefix="/sections", tags=["Legal Sections"])


# 1. CREATE SECTION
@router.post("/", response_model=LegalSectionResponse)
def create_section_route(payload: LegalSectionCreate, session: Session = Depends(get_db)):
    section = create_section(session, payload.model_dump())
    return section

# 2. GET BY ID 
@router.get("/{section_id}", response_model=LegalSectionResponse)
def get_section_route(section_id: UUID, session: Session = Depends(get_db)):
    section = get_section(session, section_id)

    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return section
    
# 3. GET SECTION BY CASE ID
@router.get("/case/{case_id}", response_model=list[LegalSectionResponse])
def get_sections_by_case_route(case_id: UUID, session: Session = Depends(get_db)):
    return get_sections_by_case(session, case_id)

# 4. UPDATE 
@router.patch("/{section_id}", response_model=LegalSectionResponse)
def update_section_route(section_id: UUID, payload: LegalSectionUpdate, session: Session = Depends(get_db)):
    section = update_section(session, section_id, payload.model_dump(exclude_unset=True))

    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    
    return section

# 5. VERIFY BY LAWYER
@router.patch("/{section_id}/verify", response_model=LegalSectionResponse)
def verify_section_route(section_id: UUID, session: Session = Depends(get_db)):
    section = verify_section(session, section_id)

    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    
    return section

# 6. DELETE
@router.delete("/{section_id}", response_model=LegalSectionResponse)
def delete_section_route(section_id: UUID, session: Session = Depends(get_db)):
    section = delete_section(session, section_id)

    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")

    return section