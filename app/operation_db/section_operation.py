from sqlmodel import Session, select
from app.models.legal_sections import LegalSection
from app.models.case_model import Case
from uuid import UUID
from app.operation_db.base_operation import create, update_and_change, soft_delete
from app.controllers.legal_controller import generate_sections
from app.models.legal_sections import SectionSource
from typing import TYPE_CHECKING
from app.operation_db.case_operation import get_case


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

def get_verified_sections(session: Session, case_id: UUID) -> LegalSection | None:
    query = select(LegalSection).where(
        LegalSection.has_lawyer_verified == True, LegalSection.is_deleted == False,
        LegalSection.case_id == case_id
        )

    verified_sections = session.exec(query).all()
    return verified_sections




def update_section(session: Session, section_id: UUID,data: dict ) -> LegalSection | None :
    section = get_section(session, section_id)

    return update_and_change(session, section, data)



def delete_section(session: Session, section_id: UUID) -> LegalSection | None:
    section = get_section(session, section_id)
    
    return soft_delete(session, section)


def generate_and_save_sections(session: Session, case_id: UUID):
    case = get_case(session, case_id)
    if case is None:
        return None
    
    if case.lawyer_approved_summary is None:
        return None
    
    result = generate_sections(case.lawyer_approved_summary)
    

    # print("RESULT = ", result)
    if result is None:
        raise Exception("generate_sections returned None")

    for item in result["sections"]:
        create_section(
            session, {
                "case_id": case.id,
                "ipc_section":item["ipc_section"],
                "bns_section": item["bns_section"],
                "reason": item["reason"],
                "source": SectionSource.llm
            }
        )

    return get_sections_by_case(session, case.id)

def verify_all_sections(session: Session, case_id: UUID):
    sections = get_sections_by_case(session, case_id)

    for section in sections:
        section.has_lawyer_verified = True
    session.commit()
    return sections    

    

