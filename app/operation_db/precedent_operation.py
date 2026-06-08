from sqlmodel import Session, select
from app.models.precedentCase_model import PrecedentCase
from app.models.case_model import Case
from uuid import UUID
from typing import List
from app.operation_db.base_operation import create, update_and_change, soft_delete
from app.operation_db.case_operation import get_case
from app.services.kanoon_service import get_case_references
from app.operation_db.section_operation import get_verified_sections

# 1. CREATE PRECEDENT
def create_precedent(session: Session, data: dict) -> PrecedentCase:
    precedent = PrecedentCase(**data)
    return create(session, precedent)

#2. GET PRECEDENTS BY CASE
def get_precedents_by_case(session: Session, case_id: UUID) -> List[PrecedentCase]:
    query = select(PrecedentCase).where(PrecedentCase.case_id == case_id, PrecedentCase.is_deleted == False)

    precedents = session.exec(query).all()
    return precedents

#3 SAVE PRECEDENTS
def generate_and_save_precedents(session: Session, case_id: UUID):
    case = get_case(session, case_id)
    if case is None:
        return None
    if case.lawyer_approved_summary is None:
        return None
    
    query = []
    sections = get_verified_sections(session, case_id)
    for section in sections:
        if section.ipc_section:
            query.append(section.ipc_section)
        if section.bns_section:
            query.append(section.bns_section)

    search_query = " ".join(query)
    
    precedents = get_case_references(search_query)
    if precedents is None:
        raise Exception("generate_precedent returns None")
    
    for item in precedents:
        create_precedent(
            session, {
                "case_id": case.id,
                "title": item["title"],
                "court": item["court"],
                "year": item["year"],
                "citation": item["citation"],
                "source": "indian_kanoon"
            }
        )
    return get_precedents_by_case(session, case.id)   

#4 . GET PRECEDENT
def get_precedent(session: Session, precedent_id: UUID) -> PrecedentCase | None :
    query = select(PrecedentCase).where(PrecedentCase.id == precedent_id, PrecedentCase.is_deleted == False)
    precedent = session.exec(query).first()
    return precedent


#5. DELTE PRECEDENT
def delete_precedent(session: Session, precedent_id: UUID) -> PrecedentCase | None :
    precedent = get_precedent(session, precedent_id)

    return soft_delete(session, precedent)