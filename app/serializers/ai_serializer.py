# app/serializers/user_serializer.py

from pydantic import BaseModel, Field
from typing import List

# SWAGGER INPUT MODEL
class CaseAnalysisRequest(BaseModel):
    case_text: str = Field(
        ..., 
        example="Three masked men entered a bank at 2:00 PM, held the cashier at gunpoint, stole 10 Lakh rupees, and shot a guard in the leg while fleeing in a stolen car."
    )

# SUB-MODELS (To structure the exact JSON format of your prompt)
class SectionDetail(BaseModel):
    section: str
    title: str
    probability: float
    reason: str

class SpecialLawDetail(BaseModel):
    act_name: str
    applicable_provisions: str
    probability: float
    reason: str

# NEW SUB-MODELS FOR REFERENCE CASES
class HistoricalSectionDetail(BaseModel):
    ipc_section: str
    bns_equivalent: str

class ReferenceCaseDetail(BaseModel):
    title: str
    case_summary_snippet: str
    historical_sections_applied: List[HistoricalSectionDetail]
    relevance: str

# SWAGGER OUTPUT MODEL (Perfect match with your prompt schema)
# This is the response we will get at frontend
class CaseAnalysisResponse(BaseModel):
    primary_offense: str
    case_summary: str  # <-- Added missing field to prevent validation errors
    ipc_sections: List[SectionDetail]
    bns_sections: List[SectionDetail]
    special_and_local_laws: List[SpecialLawDetail]
    reference_cases: List[ReferenceCaseDetail]  # <-- Added reference cases array
    overall_reasoning: str
    overall_severity: str
    cognizable: bool

































































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
 