from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
import uuid

from app.db.database import get_session
from app.serializers.ai_serializer import SectionReviewRequest, SectionReviewResponse

# 🎯 SIRF EK CONTROLLER IMPORT KIYA
from app.controllers.section_review import process_section_review

router = APIRouter(prefix="/approve", tags=["Approve"])

@router.patch("/sections/{section_id}/review", response_model=SectionReviewResponse)
def api_review_legal_section(
    section_id: uuid.UUID,
    request: SectionReviewRequest,
    session: Session = Depends(get_session)
):
    try:
        # 1. 🧠 Fat Controller Call: DB update aur logic dono yahan handle ho gaye
        result = process_section_review(
            session=session,
            section_id=section_id,
            is_approved=request.is_approved,
            rejection_reason=request.rejection_reason
        )
        
        updated_section = result["updated_section"]

        # 2. 🌐 Frontend Response
        return SectionReviewResponse(
            message="Section review updated successfully.",
            section_id=updated_section.id,
            is_approved=updated_section.is_approved,
            rejection_reason=updated_section.rejection_reason,
            section_name=result["sec_name"],         # 🎯 Controller se aayi value
            title=updated_section.title,
            probability=updated_section.probability,
            reason=updated_section.reason
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reviewing section: {str(e)}")