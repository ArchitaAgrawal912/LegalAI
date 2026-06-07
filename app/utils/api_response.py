from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uuid

T = TypeVar("T")

class BaseApiResponse(BaseModel, Generic[T]):
    status: str 
    message: str
    data: Optional[T] = None
    details: Optional[Any] = None

def success_response(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
    response_obj = BaseApiResponse(status="success", message=message, data=data)
    
    # 🎯 .model_dump(mode='json') use karo!
    # Ye automatically UUIDs, datetimes, etc. ko JSON friendly format (str) mein convert kar deta hai
    return JSONResponse(
        status_code=status_code, 
        content=response_obj.model_dump(mode='json', exclude_none=True)
    )

def error_response(message: str, status_code: int = 400, details: Any = None) -> JSONResponse:
    response_obj = BaseApiResponse(status="error", message=message, details=details)
    
    return JSONResponse(
        status_code=status_code, 
        content=response_obj.model_dump(mode='json', exclude_none=True)
    )