from sqlmodel import Session, select
from app.models.legal_sections import LegalSection
from uuid import UUID
from app.operation_db.base_controller import create, update_and_change, soft_delete

def get_section(session: Session, case_id: UUID) -> LegalSection:
    query = select(LegalSection).where(LegalSection.case_id == case_id, LegalSection.is_deleted == False)
    section = session.exec(query).first()
    return section



def get_section_by_id(session: Session,  case_id: UUID) -> LegalSection:
    return session.get(LegalSection, case_id)



def lawyer_verified(session: Session, case_id: UUID) -> LegalSection:
    section = get_section(session, case_id)
    section.has_lawyer_verified = True
    return create(session, section) # commit + refresh



def update_section(session: Session, case_id: UUID, **kwargs) -> LegalSection | None :
    section = get_section(session, case_id)
    if section is None:
        return None
    return update_and_change(session, section, kwargs)



def delete_section(session: Session, case_id: UUID) -> LegalSection:
    section = get_section(session, case_id)
    if section is None:
        return None
    return soft_delete(session, section)


