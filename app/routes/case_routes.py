from fastapi import APIRouter, Depends
from sqlmodel import Session
import uuid
from typing import List

from app.db.database import get_session
from app.models.crud import get_cases_by_user, search_cases 
# 🎯 Naye imports
from app.serializers.legal_case_serializer import CaseResponse
from app.utils.api_response import success_response, error_response

router = APIRouter(prefix="/cases", tags=["Cases"])

# ==========================================
# 3. GET ALL CASES OF A USER (WITH PAGINATION)
# ==========================================
@router.get("/user/{user_id}")
def api_get_user_cases(
    user_id: uuid.UUID, 
    offset: int = 0, 
    limit: int = 10,
    session: Session = Depends(get_session)
):
    try:
        cases = get_cases_by_user(session=session, user_id=user_id, offset=offset, limit=limit)
        
        # Empty list handling
        if not cases:
            return success_response(data=[], message="No cases found for this user.")

        return success_response(data=cases, message="Cases fetched successfully.")
        
    except Exception as e:
        return error_response(message="Error fetching cases", status_code=500, details=str(e))


# ==========================================
# 4. SEARCH CASES (Keyword & Filters)
# ==========================================
@router.get("/search/")
def api_search_cases(
    keyword: str | None = None,
    user_id: uuid.UUID | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    try:
        cases = search_cases(
            session=session, 
            user_id=user_id, 
            keyword=keyword, 
            offset=offset, 
            limit=limit
        )
        
        if not cases:
            return success_response(data=[], message="No cases found matching your criteria.")

        return success_response(data=cases, message="Search successful.")
        
    except Exception as e:
        return error_response(message="Search failed", status_code=500, details=str(e))


























#  ye route case ko lega user se , controller bulayega and  vha se jo response aaya usery  new_case me daalega  and then usey  created_cases.append(new_case) ki help

#   se array me daalega and response return kardega 


#  create case function controller me hai

#  is file  me sab route ke aage prefix cases lagega


#  here session is vhi jo db/database.py me bnaya humne 
 #  tags=["Cases"]: Yeh sirf Swagger UI (/docs) ke liye hai. Isse Swagger par saare case waale routes ek sundar se folder/group ("Cases") ke andar dikhte hain.