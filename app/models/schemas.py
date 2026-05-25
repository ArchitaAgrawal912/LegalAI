from pydantic import BaseModel, Field

class CaseRequest(BaseModel):
    case_description: str = Field(
        ..., 
        min_length=10, 
        description="The facts of the legal incident to be analyzed."
    )

class LegalSection(BaseModel):
    ipc_section: str = Field(description="The applicable Indian Penal Code (IPC) section, e.g., 'Section 378'")
    bns_equivalent: str = Field(description="The equivalent section in the Bharatiya Nyaya Sanhita (BNS), e.g., 'Section 303(2)'")
    offense: str = Field(description="The name of the crime, e.g., 'Theft'")
    explanation: str = Field(description="A brief, precise legal explanation of why this section applies to the provided facts.")

class CaseResponse(BaseModel):
    case_summary: str = Field(description="A concise one-sentence legal summary of the incident.")
    applicable_charges: list[LegalSection] = Field(description="Comprehensive list of all applicable penal charges.")