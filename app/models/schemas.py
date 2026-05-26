# Whenever data comes into your app (from the user) or goes out of your app (from the AI or Kanoon),
#  this file stops it, measures it, and makes sure it fits the exact shapes defined here.


# BaseModel is a pre-built engine provided by a Python library called Pydantic. It does all the heavy, boring work of inspecting and verifying data

from pydantic import BaseModel, Field

class CaseRequest(BaseModel):
    case_description: str = Field(
        ..., 
        min_length=10, 
        description="The facts of the legal incident to be analyzed."
    )
# It si embedded in case response and is used to define the shape of the data that the AI will return for each legal section it identifies.
class LegalSection(BaseModel):
    ipc_section: str = Field(description="The applicable Indian Penal Code (IPC) section, e.g., 'Section 378'")
    bns_equivalent: str = Field(description="The equivalent section in the Bharatiya Nyaya Sanhita (BNS), e.g., 'Section 303(2)'")
    offense: str = Field(description="The name of the crime, e.g., 'Theft'")
    explanation: str = Field(description="A brief, precise legal explanation of why this section applies to the provided facts.")

# This is the new schema for the precedent cases we will fetch from Kanoon. Each case has a title, a unique document ID, a brief snippet, and a URL to the full case on Indian Kanoon.
class ReferenceCase(BaseModel):
    title: str = Field(description="The title of the court case.")
    doc_id: str = Field(description="The Indian Kanoon document ID.")
    snippet: str = Field(description="A brief text snippet from the judgment.")
    url: str = Field(description="The full URL to the Indian Kanoon document.")

# Update your existing CaseResponse to include the new list
class CaseResponse(BaseModel):
    case_summary: str = Field(description="A concise one-sentence legal summary of the incident.")
    applicable_charges: list[LegalSection] = Field(description="Comprehensive list of all applicable penal charges.")
    # NEW: We make this optional so the AI doesn't try to generate it. 
    # We will populate it manually from the Kanoon API.
    precedent_cases: list[ReferenceCase] | None = None

