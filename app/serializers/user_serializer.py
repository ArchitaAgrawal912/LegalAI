from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime

# ==========================================
# FRONTEND SE AANE WALA DATA (Input)
# ==========================================
class UserCreate(BaseModel):
    name: str  # 'username' aur 'full_name' ko milakar sirf 'name' kar diya
    email: EmailStr
    phone_no: str   # DB model ke hisaab se add kiya
    password: str  # Frontend plain text bhejega, hum route me hash karenge

# ==========================================
# FRONTEND KO JANE WALA DATA (Output)
# ==========================================
class UserResponse(BaseModel):
    id: uuid.UUID
    name: str  # Yahan bhi sirf 'name'
    email: EmailStr
    phone_no: str | None = None  # DB model ke hisaab se add kiya
    is_active: bool
    created_at: datetime

    # 🎯 Notice: Yahan password_hash missing hai, for security!

    #  note ye sab yha serializer me and model me dono me validation defined hai , yha hai for api route jab route listen req
    #  and models me validation are for tables , ki table ke rule kya honge 