from fastapi import APIRouter, Depends
from sqlmodel import Session
import uuid

from app.db.database import get_session
# 🎯 Naye imports
from app.serializers.ai_serializer import SectionReviewRequest, SectionReviewResponse
from app.controllers.section_review import process_section_review
from app.utils.api_response import success_response, error_response

router = APIRouter(prefix="/approve", tags=["Approve"])

@router.patch("/sections/{section_id}/review")
def api_review_legal_section(
    section_id: uuid.UUID,
    request: SectionReviewRequest,
    session: Session = Depends(get_session)
):
    try:
        # 1. Controller Call
        result = process_section_review(
            session=session,
            section_id=section_id,
            is_approved=request.is_approved,
            rejection_reason=request.rejection_reason
        )
        
        updated_section = result["updated_section"]

        # 2. Validation: Data ko Schema se validate kiya
        response_data = SectionReviewResponse(
            message="Section review updated successfully.",
            section_id=updated_section.id,
            is_approved=updated_section.is_approved,
            rejection_reason=updated_section.rejection_reason,
            section_name=result["sec_name"],
            title=updated_section.title,
            probability=updated_section.probability,
            reason=updated_section.reason
        )

        # 3. Standardized Success Response
        return success_response(
            data=response_data,
            message="Section review processed successfully"
        )

    except ValueError as ve:
        # Jab section nahi mila (404 scenario)
        return error_response(
            message="Section not found", 
            status_code=404, 
            details=str(ve)
        )
        
    except Exception as e:
        session.rollback()
        # 4. Standardized Error Response
        return error_response(
            message="Error reviewing section", 
            status_code=500, 
            details=str(e)
        )