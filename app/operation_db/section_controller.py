from sqlmodel import Session, select
from app.models.legal_sections import LegalSection
from uuid import UUID
from app.operation_db.base_controller import create, update_and_change, soft_delete


def create_section(session: Session, data: dict) -> LegalSection:
    section = LegalSection(**data)
    return create(session, section)


def get_section(session: Session, section_id: UUID) -> LegalSection | None:
    query = select(LegalSection).where(LegalSection.id == section_id, LegalSection.is_deleted == False)
    section = session.exec(query).first()
    return section


def get_sections_by_case(session: Session, case_id: UUID) -> list[LegalSection]:
    query = select(LegalSection).where(LegalSection.case_id == case_id, LegalSection.is_deleted == False)

    sections = session.exec(query).all()
    return sections


# def get_section_by_id(session: Session,  case_id: UUID) -> LegalSection:
#     return session.get(LegalSection, case_id)



def verify_section(session: Session, section_id: UUID) -> LegalSection | None:
    section = get_section(session, section_id)
    if section is None:
        return None
    section.has_lawyer_verified = True
    return create(session, section) # commit + refresh



def update_section(session: Session, section_id: UUID,data: dict ) -> LegalSection | None :
    section = get_section(session, section_id)

    return update_and_change(session, section, data)



def delete_section(session: Session, section_id: UUID) -> LegalSection | None:
    section = get_section(session, section_id)
    
    return soft_delete(session, section)


