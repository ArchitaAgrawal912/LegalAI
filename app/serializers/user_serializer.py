from pydantic import BaseModel, Field
from typing import List

# SWAGGER INPUT MODEL
class CaseAnalysisRequest(BaseModel):
    case_text: str = Field(
        # ... means this field is compulsary
        ..., 
        #  emaple shows dummy text on swagger
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

# SWAGGER OUTPUT MODEL (Perfect match with your prompt schema)
#  this is the response we will get at fronend  
class CaseAnalysisResponse(BaseModel):
    #  since ipc can have further legal sections so we wrap it in list 
    ipc_sections: List[SectionDetail]
    bns_sections: List[SectionDetail]
    special_and_local_laws: List[SpecialLawDetail]
    primary_offense: str
    #  overall reasoning is the summary we get
    overall_reasoning: str
    overall_severity: str
    cognizable: bool


































































#  serializerss do 3 works

#     Frontend se aane wale data ka chehra check karna (Input Validation).(agar hume text chye toh
#  user tect de naa ki number daalde uspe agar daala toh error aayega)

# Backend se jaane wale data ko sahi tarike se wrap karna (Output Serialization).

# Swagger ko design dena (Documentation).( ki get kaisa dikhega and post kaisa dikhega)

#  what is base model here
# Pydantic library se aane wali ek predefined Python class hai. 
# Pydantic Python ka sabse popular data validation package hai,
#  if kisi class me base model aagya toh that class become powerful
# check ki user ne text hi aala na khi string text ki jagah int na daala ho , varna error do
#  base model has serialization power like it take frontend ka json and convert to python obj
#  so that backend can read it