import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

# ==========================================
# 🎯 SECTION DETAILS (For List Generation)
# ==========================================
class SectionDetail(BaseModel):
    section: str = Field(example="Section 378")
    title: str = Field(example="Theft")
    probability: float = Field(example=0.95)
    reason: str = Field(example="Because the phone was snatched without consent.")

# ==========================================
# ⚖️ API 2: ANALYZE CHARGES
# ==========================================
class ChargeAnalysisRequest(BaseModel):
    case_id: uuid.UUID
    lawyer_approved_summary: str

class ChargeAnalysisResponse(BaseModel):
    message: str
    # 🎯 Yahan list aayegi jisme bohot saare sections honge!
    ipc_sections: List[SectionDetail]
    bns_sections: List[SectionDetail]

# ==========================================
# ✅ API 3: APPROVE/REJECT REVIEW
# ==========================================
class SectionReviewRequest(BaseModel):
    is_approved: bool
    rejection_reason: str | None = None

class SectionReviewResponse(BaseModel):
    message: str
    section_id: uuid.UUID
    is_approved: bool
    rejection_reason: str | None
    
    # Frontend display ke liye poori detail wapas bhej rahe hain
    section_name: str 
    title: str
    probability: float
    reason: str




class CaseAnalysisRequest(BaseModel):
    user_id: uuid.UUID = Field(
        ..., 
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    raw_description: str = Field(
        ..., 
        example="On 15th May, my iPhone was snatched by two unknown men on a bike..."
    )

# ==========================================
class CaseAnalysisResponse(BaseModel):
    case_id: uuid.UUID 
    title: str = Field(
        example="Mobile Snatching and Physical Assault"
    )
    llm_summary: str = Field(
        example="The complainant reported an incident where two unidentified individuals snatched an iPhone 14..."
    )



















































#  serializerss do 3 works

#     Frontend se aane wale data ka chehra check karna (Input Validation).(agar hume text chye toh
#  user text de naa ki number daalde uspe agar daala toh error aayega)

# Backend se jaane wale data ko sahi tarike se wrap karna (Output Serialization).

# Swagger ko design dena (Documentation).( ki get kaisa dikhega and post kaisa dikhega)

#  what is base model here
# Pydantic library se aane wali ek predefined Python class hai. 
# Pydantic Python ka sabse popular data validation package hai,
#  if kisi class me base model aagya toh that class become powerful
# check ki user ne text hi aala na khi string text ki jagah int na daala ho , varna error do
#  base model has serialization power like it take frontend ka json and convert to python obj
#  so that backend can read it
 #  base model class se hi python output obj ko json me convert karta 
 