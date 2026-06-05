from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid
from typing import List, Optional  # 🎯 Optional import kiya yahan

from app.db.database import get_session
from app.models.crud import create_case, get_cases_by_user , search_cases # 🎯 search_cases import kiya yahan
from app.serializers.legal_case_serializer import CaseCreate, CaseResponse

# Router for cases
router = APIRouter(prefix="/cases", tags=["Cases"])

# ==========================================
# 1. BULK CASE ROUTE (Array of Cases daalne ke liye)
# ==========================================
@router.post("/bulk", response_model=List[CaseResponse])
def api_create_multiple_cases(cases_data: List[CaseCreate], session: Session = Depends(get_session)):
    try:
        created_cases = []
        for data in cases_data:
            # Naye model ke hisaab se fields update kar di
            new_case = create_case(
                session=session,
                title=data.title,
                raw_description=data.raw_description,
                user_id=data.user_id
                # Note: 'status' DB apne aap "pending" set kar dega
            )
            created_cases.append(new_case)
        return created_cases
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bulk Case Error: {str(e)}")

# ==========================================
# 2. SINGLE CASE ROUTE (Sirf 1 Case daalne ke liye)
# ==========================================
# @router.post("/", response_model=CaseResponse)
# def api_create_single_case(case_data: CaseCreate, session: Session = Depends(get_session)):
#     try:
#         new_case = create_case(
#             session=session,
#             title=case_data.title,
#             raw_description=case_data.raw_description,
#             user_id=case_data.user_id
#         )
#         return new_case
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Case Error: {str(e)}")


# ==========================================
# 3. GET ALL CASES OF A USER (WITH PAGINATION)
# ==========================================
@router.get("/user/{user_id}", response_model=List[CaseResponse])
def api_get_user_cases(
    user_id: uuid.UUID, 
    offset: int = 0,           # Default: 0 (Pehle record se shuru karo)
    limit: int = 10,          # Default: 10 (Ek baar me 10 cases dikhao)
    session: Session = Depends(get_session)
):
    try:
        # CRUD function call kiya pagination parameters ke sath
        cases = get_cases_by_user(session=session, user_id=user_id, offset=offset, limit=limit)
        return cases
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching cases: {str(e)}")


# ==========================================
# 4. SEARCH CASES (Keyword & Filters)
# ==========================================
@router.get("/search/", response_model=List[CaseResponse])
def api_search_cases(
    keyword: str|None = None,     # Optional: Agar search box khali ho
    user_id: uuid.UUID|None= None, # Optional: Specific user ke liye filter
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
        return cases
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")


































#  ye route case ko lega user se , controller bulayega and  vha se jo response aaya usery  new_case me daalega  and then usey  created_cases.append(new_case) ki help

#   se array me daalega and response return kardega 


#  create case function controller me hai

#  is file  me sab route ke aage prefix cases lagega


#  here session is vhi jo db/database.py me bnaya humne 
 #  tags=["Cases"]: Yeh sirf Swagger UI (/docs) ke liye hai. Isse Swagger par saare case waale routes ek sundar se folder/group ("Cases") ke andar dikhte hain.