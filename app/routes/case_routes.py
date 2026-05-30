from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid
from typing import List
from app.db.database import get_session
from app.controllers.crud import create_case
from app.serializers.legal_case_serializer import CaseCreate, CaseResponse

# Router for cases
router = APIRouter(prefix="/cases", tags=["Cases"])

# Case Banane Ka Route
@router.post("/bulk", response_model=List[CaseResponse])
def api_create_multiple_cases(cases_data: List[CaseCreate], session: Session = Depends(get_session)):
    try:
        created_cases = []
        for data in cases_data:
            new_case = create_case(
                session=session,
                case_number=data.case_number,
                title=data.title,
                description=data.description,
                created_by=data.created_by
            )
            created_cases.append(new_case)
        return created_cases
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bulk Case Error: {str(e)}")






#  ye route case ko lega user se , controller bulayega and  vha se jo response aaya usery  new_case me daalega  and then usey  created_cases.append(new_case) ki help

#   se array me daalega and response return kardega 


#  create case function controller me hai

#  is file  me sab route ke aage prefix cases lagega


#  here session is vhi jo db/database.py me bnaya humne 
 #  tags=["Cases"]: Yeh sirf Swagger UI (/docs) ke liye hai. Isse Swagger par saare case waale routes ek sundar se folder/group ("Cases") ke andar dikhte hain.