from fastapi import APIRouter, Depends
from sqlmodel import Session
import uuid
from pydantic import BaseModel

from app.db.database import get_session
from app.models.legal_case import LegalCase
from app.controllers.reference_cases import generate_and_save_references
from app.utils.api_response import success_response, error_response

# 1. Naya chhota request model (Only what is needed)
class ReferenceFetchRequest(BaseModel):
    case_id: uuid.UUID

router = APIRouter(prefix="/references", tags=["Reference Cases"])

@router.post("/fetch")
async def api_fetch_case_references(
    request: ReferenceFetchRequest, 
    session: Session = Depends(get_session)
):
    case = session.get(LegalCase, request.case_id)
    if not case:
        return error_response(message="Case not found", status_code=404)

    # 🚨 Edge Case Guard: Agar case mein ek bhi section nahi hai
    if not case.sections:
         return error_response(message="No sections found to review.", status_code=400)

    # 🛡️ THE NEW GUARD: Find sections where lawyer hasn't verified yet
    pending_sections = [s for s in case.sections if not s.has_lawyer_verified]
    
    # Agar pending list mein kuch bhi hai, toh rok do
    if len(pending_sections) > 0:
        return error_response(
            message="Access Denied",
            status_code=403,
            details=f"Please verify all sections. {len(pending_sections)} section(s) pending review."
        )

    try:
        # 🧠 Controller Call
        precedents = await generate_and_save_references(
            session=session, 
            case_id=request.case_id
        )
        
        if not precedents:
            return success_response(data=[], message="No relevant legal precedents found.", status_code=200)

        return success_response(
            data=precedents, 
            message="References fetched successfully based on verified sections."
        )
        
    except Exception as e:
        return error_response(message="Reference Fetch Error", status_code=500, details=str(e))