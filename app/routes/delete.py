import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.models import crud
from app.utils.api_response import success_response, error_response

router = APIRouter(prefix="/delete", tags=["Delete Operations"])

# 1. Generic helper for delete operations to keep code clean
def perform_delete(operation_func, session: Session, item_id: uuid.UUID, item_name: str):
    try:
        if not operation_func(session, item_id):
            return error_response(f"{item_name} not found", status_code=404)
        
        session.commit() # Ensure changes are saved
        return success_response(data=None, message=f"{item_name} deleted successfully.")
    except Exception as e:
        session.rollback()
        return error_response(f"Error deleting {item_name.lower()}", status_code=500, details=str(e))

# 2. Updated Routes
@router.delete("/case/{case_id}")
def api_delete_case(case_id: uuid.UUID, session: Session = Depends(get_session)):
    return perform_delete(crud.delete_case, session, case_id, "Case")

@router.delete("/section/{section_id}")
def api_delete_section(section_id: uuid.UUID, session: Session = Depends(get_session)):
    return perform_delete(crud.delete_legal_section, session, section_id, "Section")

@router.delete("/reference/{ref_id}")
def api_delete_reference(ref_id: uuid.UUID, session: Session = Depends(get_session)):
    return perform_delete(crud.delete_reference, session, ref_id, "Reference case")

@router.delete("/user/{user_id}")
def api_delete_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    return perform_delete(crud.delete_user_account, session, user_id, "User account")