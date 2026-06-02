from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid

from app.db.database import get_session
from app.models.crud import update_section_approval
from app.serializers.ai_serializer import SectionReviewRequest, SectionReviewResponse

router = APIRouter(prefix="/approve", tags=["Approve"])

@router.patch("/sections/{section_id}/review", response_model=SectionReviewResponse)
def api_review_legal_section(
    section_id: uuid.UUID,
    request: SectionReviewRequest,
    session: Session = Depends(get_session)
):
    try:
        # 1. DB mein approve/reject status update karwa liya
        updated_section = update_section_approval(
            session=session,
            section_id=section_id,
            is_approved=request.is_approved,
            rejection_reason=request.rejection_reason
        )

        # 2. Smart Logic: Pata lagao ki IPC bhejna hai ya BNS
        # Agar IPC "N/A" nahi hai, toh IPC naam do, warna BNS naam do
        sec_name = updated_section.ipc_section if updated_section.ipc_section != "N/A" else updated_section.bns_section

        # 3. 🎯 Full Response bhej rahe hain jisme saare Pydantic fields hain
        return SectionReviewResponse(
            message="Section review updated successfully.",
            section_id=updated_section.id,
            is_approved=updated_section.is_approved,
            rejection_reason=updated_section.rejection_reason,
            section_name=sec_name,               # Naya field
            title=updated_section.title,         # Naya field
            probability=updated_section.probability, # Naya field
            reason=updated_section.reason        # Naya field
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reviewing section: {str(e)}")