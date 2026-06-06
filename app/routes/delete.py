import uuid # 🎯 Import zaroori hai!
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import get_session
from app.models import crud

router = APIRouter(prefix="/delete", tags=["Delete Operations"])

# 1. Delete Case (Case + References + Sections)
@router.delete("/case/{case_id}")
def api_delete_case(case_id: uuid.UUID, session: Session = Depends(get_session)):
    if not crud.delete_case(session, case_id):
        raise HTTPException(status_code=404, detail="Case not found")
    return {"message": "Case and all associated data deleted successfully"}

# 2. Delete Section
@router.delete("/section/{section_id}")
def api_delete_section(section_id: uuid.UUID, session: Session = Depends(get_session)):
    if not crud.delete_legal_section(session, section_id):
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Section deleted"}

# 3. Delete Reference Case
@router.delete("/reference/{ref_id}")
def api_delete_reference(ref_id: uuid.UUID, session: Session = Depends(get_session)):
    if not crud.delete_reference(session, ref_id):
        raise HTTPException(status_code=404, detail="Reference case not found")
    return {"message": "Reference case deleted"}

# 4. Delete User (User + Cases + Sections + References)
@router.delete("/user/{user_id}")
def api_delete_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    if not crud.delete_user_account(session, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User account and all data deleted successfully"}