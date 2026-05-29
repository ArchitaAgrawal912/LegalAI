import uuid
from sqlmodel import Session, select
from app.models.ipc_section_table import IpsSection

# ==========================================
# 1. CREATE
# ==========================================
def create_ips_section(session: Session, section_code: str, section_name: str, case_id: uuid.UUID, description: str = None, penalty: str = None) -> IpsSection:
    new_section = IpsSection(
        section_code=section_code,
        section_name=section_name,
        description=description,
        penalty=penalty,
        case_id=case_id
    )
    session.add(new_section)
    session.commit()
    session.refresh(new_section)
    return new_section

# ==========================================
# 2. READ
# ==========================================
def get_ips_section_by_id(session: Session, section_id: uuid.UUID) -> IpsSection | None:
    return session.get(IpsSection, section_id)

def get_sections_by_case(session: Session, case_id: uuid.UUID) -> list[IpsSection]:
    # Ek specific case ki saari dharayein nikalne ke liye
    statement = select(IpsSection).where(IpsSection.case_id == case_id)
    return session.exec(statement).all()

# ==========================================
# 3. UPDATE
# ==========================================
def update_ips_section(session: Session, section_id: uuid.UUID, **kwargs) -> IpsSection | None:
    section = session.get(IpsSection, section_id)
    if not section:
        return None
    
    for key, value in kwargs.items():
        setattr(section, key, value)
        
    session.add(section)
    session.commit()
    session.refresh(section)
    return section

# ==========================================
# 4. DELETE
# ==========================================
def delete_ips_section(session: Session, section_id: uuid.UUID) -> bool:
    section = session.get(IpsSection, section_id)
    if not section:
        return False
        
    session.delete(section)
    session.commit()
    return True