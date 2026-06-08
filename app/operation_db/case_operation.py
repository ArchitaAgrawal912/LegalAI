from sqlmodel import Session, select
from uuid import UUID
from typing import TYPE_CHECKING
from app.models.case_model import Case
from app.controllers.summary_controller import generate_case_summary
from app.operation_db.base_operation import create, update_and_change, soft_delete



# 1.>>>>>>>>>>> CREATE >>>>>>>>>>>>>
def create_case(session: Session, data: dict) -> Case:
    # raw description first save
    case = Case(**data)
    create(session, case)
    # LLM call
    result = generate_case_summary(case.case_description)
    # Summary Save 
    return update_and_change(session, case, {
        "title": result["title"],
        "llm_summary": result["summary"]
    })
    

# (**data) -> Ye dictionary ko Case object me convert kar raha hai.

# 2. >>>>>>>>>>>>> GET >>>>>>>>>>>>
def get_case(session: Session, id: UUID) -> Case | None:
    query = select(Case).where(Case.id == id, Case.is_deleted == False)
    case = session.exec(query).first()

    return case


# 3. >>>>>>>>>>>>>> UPDATE >>>>>>>>>>>>>
def update_case(session: Session, id: UUID, data: dict) -> Case | None:
    case = get_case(session, id)
    
    return update_and_change(session, case, data)
    
    

# 4. >>>>>>>>>>>>>> DELETE >>>>>>>>>>>>>>
def delete_case(session: Session, id: UUID) -> Case | None:
    case = get_case(session, id)
    
    return soft_delete(session, case)

# 5. GET ALL CASES WITH SEARCH
def get_all_cases(session: Session, user_id: UUID, search: str = None, page: int = 1, limit: int = 10) -> list[Case]:
    query = select(Case).where(Case.user_id == user_id, Case.is_deleted == False)

    if search:
        query = query.where(
            Case.case_description.ilike(f"%{search}%") | 
            Case.title.ilike(f"%{search}%")                     
        )
    offset = (page - 1) * limit

    cases = session.exec(query.offset(offset).limit(limit)).all()
    
    return cases

# 6. APPROVE SUMMARY
def approve_summary(session: Session, case_id: UUID) -> Case | None:
    from app.operation_db.section_operation import generate_and_save_sections
    case = get_case(session, case_id)
    if case is None:
        return None
    case = update_and_change(session, case, {"lawyer_approved_summary":case.llm_summary})

    generate_and_save_sections(session, case.id)

    return case

# 7. REJECT/EDIT summary
def review_summary(session: Session, case_id: UUID, summary: str) -> Case | None:
    case = get_case(session, case_id)
    if case is None:
        return None
    case = update_and_change(session, case, {"lawyer_approved_summary": summary})

    generate_and_save_sections(session, case.id)

    return case















# # 8. REJECT SUMMARY
# def reject_summary(session: Session, case_id: UUID) -> Case | None:
#     case = get_case(session, case_id)
#     if case is None:
#         return None
#     case.llm_summary = None

#     return update_and_change(session, case, {"lawyer_approved_summary": summary})




# % → SQL Wildcard : Is jagah kuch bhi ho sakta hai.

# Kitna data chhodna hai? → offset
# Kitna data lena hai? → limit

# Session = Database Conversation
# Session bolta hai:
#"Main database se connected hoon."


# # 6. LLM SUMMARY GET 
# def generate_and_save_summary(session: Session, case_id: UUID) -> Case | None:

#     # Fetcing the case....
#     case = get_case(session, case_id)
#     if case is None:
#         return  None
    
#     # LLM call
#     result = generate_case_summary(case.case_description)

#     # Summary Save 
#     return update_and_change(session, case, {
#         "title": result["title"],
#         "llm_summary": result["summary"]
#     })
