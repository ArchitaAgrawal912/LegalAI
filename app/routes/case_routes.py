from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.services.ai_service import generate_case_summary
from app.serializers.ipc_serializer import IPCResponse
from app.serializers.review_serializer import IPCReviewRequest as LawyerDecision
from app.db.database import get_session
from app.models.case_model import Case, CaseCreate
from app.models.ipc_model import IPCSection
import httpx, json, os

router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)


# =========================================
# STEP 1: USER SUBMITS CASE → LLM PREDICTS IPC + BNS SECTIONS
# =========================================

@router.post("/", summary="STEP 1 - User submits case description")
def create_case(
    case: CaseCreate,
    session: Session = Depends(get_session)
):
    new_case = Case(
        title=case.title,
        description=case.description
    )
    session.add(new_case)
    session.commit()
    session.refresh(new_case)

    ai_result = generate_case_summary(case.description)

    validated_response = IPCResponse.model_validate(ai_result)

    saved_sections = []

    for section in validated_response.sections:
        ipc = IPCSection(
            section_number=section.section_code,
            title=section.title,
            punishment=section.punishment,
            reason=section.reason,
            lawyer_decision=None,
            case_id=new_case.id
        )
        session.add(ipc)
        saved_sections.append({
            "section_number": section.section_code,
            "title": section.title,
            "punishment": section.punishment,
            "reason": section.reason
        })

    session.commit()

    return {
        "message": "Case created. Lawyer must now review each IPC/BNS section.",
        "case_id": new_case.id,
        "predicted_sections": saved_sections
    }


# =========================================
# STEP 2: LAWYER REVIEWS ALL IPC SECTIONS OF A CASE
# =========================================

@router.get("/{case_id}/sections", summary="STEP 2A - Lawyer views all IPC sections for a case")
def get_case_sections(
    case_id: int,
    session: Session = Depends(get_session)
):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    sections = session.exec(
        select(IPCSection).where(IPCSection.case_id == case_id)
    ).all()

    return {
        "case_id": case_id,
        "case_title": case.title,
        "sections": sections,
        "instruction": "Use PATCH /ipc/{ipc_id}/review to approve or reject each section"
    }


# =========================================
# STEP 3: GENERATE FINAL REPORT AFTER LAWYER APPROVES SECTIONS
# =========================================

@router.post("/{case_id}/generate-report", summary="STEP 3 - Generate final legal summary from approved sections")
def generate_report(
    case_id: int,
    session: Session = Depends(get_session)
):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    approved_sections = session.exec(
        select(IPCSection).where(
            IPCSection.case_id == case_id,
            IPCSection.lawyer_decision == "approved"
        )
    ).all()

    if not approved_sections:
        return {"message": "No approved sections found. Use PATCH /ipc/{ipc_id}/review to approve sections first."}

    sections_text = "\n".join([
        f"- Section {s.section_number} ({s.title}): {s.reason}. Punishment: {s.punishment}"
        for s in approved_sections
    ])

    llm_prompt = f"""
You are a senior Indian legal expert.

Based on the approved IPC/BNS sections and case description below, generate a detailed legal report.

Case Description:
{case.description}

Approved IPC/BNS Sections:
{sections_text}

Return ONLY valid JSON, no markdown, no extra text in this exact format:
{{
  "summary": "A detailed 3-4 sentence legal summary explaining what happened and which laws were violated",
  "recommended_action": "Clear step by step recommended actions for the lawyer to proceed with this case",
  "past_cases": [
    "Vishaka vs State of Rajasthan (1997) - Supreme Court laid down guidelines against sexual harassment",
    "State of Punjab vs Gurmit Singh (1996) - Supreme Court on strict punishment for crimes against women",
    "Rupan Deol Bajaj vs KPS Gill (1995) - Senior IPS officer convicted for outraging modesty of woman"
  ]
}}

IMPORTANT FOR past_cases:
- Return REAL Indian court cases that are relevant to the approved IPC sections
- Format must be: "Party vs Party (Year) - one line relevance"
- Cases must be from Supreme Court or High Courts of India
- Cases must directly relate to the IPC/BNS sections that were approved
- Return exactly 3 past cases
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": llm_prompt}]
    }

    try:
        llm_response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        raw = llm_response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(raw)
    except Exception as e:
        parsed = {
            "summary": "Report generation failed. Please try again.",
            "recommended_action": str(e),
            "past_cases": []
        }

    case.final_summary = parsed.get("summary", "")
    case.final_reasoning = parsed.get("recommended_action", "")
    case.report_status = "pending_lawyer_approval"

    session.add(case)
    session.commit()
    session.refresh(case)

    return {
        "message": "Report generated. Lawyer must now approve or reject it.",
        "case_id": case.id,
        "status": case.report_status,
        "summary": case.final_summary,
        "recommended_action": case.final_reasoning,
        "similar_past_cases": parsed.get("past_cases", []),
        "next_step": "Use PATCH /cases/{case_id}/review-report to approve or reject"
    }


# =========================================
# STEP 4: LAWYER APPROVES OR REJECTS FINAL REPORT
# =========================================

@router.patch("/{case_id}/review-report", summary="STEP 4 - Lawyer approves or rejects the final report")
def review_report(
    case_id: int,
    review: LawyerDecision,
    session: Session = Depends(get_session)
):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    if review.decision not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="decision must be 'approved' or 'rejected'")

    case.report_status = review.decision
    session.add(case)
    session.commit()
    session.refresh(case)

    return {
        "message": f"Final report {review.decision} successfully.",
        "case_id": case.id,
        "report_status": case.report_status
    }


# =========================================
# HISTORY: LAWYER VIEWS ALL CASES
# =========================================

@router.get("/", summary="HISTORY - View all cases")
def get_all_cases(session: Session = Depends(get_session)):
    cases = session.exec(select(Case)).all()
    return cases


@router.get("/{case_id}/full", summary="HISTORY - View single case with all IPC sections")
def get_case_with_sections(
    case_id: int,
    session: Session = Depends(get_session)
):
    case = session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    ipc_sections = session.exec(
        select(IPCSection).where(IPCSection.case_id == case_id)
    ).all()

    return {
        "case": case,
        "ipc_sections": ipc_sections
    }


# =========================================
# OTHER CRUD (Update, Delete, Replace, Batch)
# =========================================

@router.patch("/{case_id}", summary="Update case details")
def update_case(
    case_id: int,
    updated_case: CaseCreate,
    session: Session = Depends(get_session)
):
    existing_case = session.get(Case, case_id)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")

    if updated_case.title:
        existing_case.title = updated_case.title
    if updated_case.description:
        existing_case.description = updated_case.description

    session.add(existing_case)
    session.commit()
    session.refresh(existing_case)

    return {"message": "Case updated", "data": existing_case}


@router.delete("/{case_id}", summary="Delete a case")
def delete_case(
    case_id: int,
    session: Session = Depends(get_session)
):
    existing_case = session.get(Case, case_id)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")

    session.delete(existing_case)
    session.commit()

    return {"message": f"Case {case_id} deleted successfully"}


@router.put("/{case_id}", summary="Replace full case")
def replace_case(
    case_id: int,
    updated_case: CaseCreate,
    session: Session = Depends(get_session)
):
    existing_case = session.get(Case, case_id)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")

    existing_case.title = updated_case.title
    existing_case.description = updated_case.description

    session.add(existing_case)
    session.commit()
    session.refresh(existing_case)

    return {"message": f"Case {case_id} replaced", "data": existing_case}


@router.post("/batch", summary="Create multiple cases at once")
def create_cases_batch(
    cases: List[CaseCreate],
    session: Session = Depends(get_session)
):
    created_cases = []
    for case in cases:
        new_case = Case(title=case.title, description=case.description)
        session.add(new_case)
        created_cases.append(new_case)

    session.commit()
    return {"message": "Batch cases created", "count": len(created_cases)}