from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid
from typing import List
# Tumhara DB session aur controllers
from app.db.database import get_session
from app.controllers.ipc_section_controller import create_ips_section

# Tumhare serializers
from app.serializers.ipc_serializer import IpsSectionCreate, IpsSectionResponse

# Router initialize kiya
router = APIRouter(prefix="/ipc-sections", tags=["IPC Sections"])

# ==========================================
# CREATE IPC SECTION ROUTE (POST)
# ==========================================
@router.post("/bulk", response_model=List[IpsSectionResponse])
def api_create_multiple_ipc_sections(sections_data: List[IpsSectionCreate], session: Session = Depends(get_session)):
    try:
        created_sections = []
        for data in sections_data:
            new_section = create_ips_section(
                session=session,
                section_code=data.section_code,
                section_name=data.section_name,
                description=data.description,
                penalty=data.penalty,
                case_id=data.case_id
            )
            created_sections.append(new_section)
        return created_sections
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bulk IPC Error: {str(e)}")