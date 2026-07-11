import traceback
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.errors import server_error_exc
from app.schemas.case import CaseRequest
from app.models.legal_case import LegalCase
from app.services.legal_service import LegalAnalysisService
from app.models.user import User
from fastapi import HTTPException

async def create_draft_case_controller(
    request: CaseRequest,
    current_user: User,
    db: AsyncSession,
    legal_service: LegalAnalysisService,
):
    try:
        draft_result = await legal_service.draft_summary(
            case_description=request.case_description
        )

        db_case = LegalCase(
            user_id=current_user.id,
            title=draft_result.title,
            raw_description=request.case_description,
            llm_summary=draft_result.summary,
            status="pending_review",
        )

        db.add(db_case)
        await db.commit()
        await db.refresh(db_case)

        return db_case

    except Exception:
        traceback.print_exc()
        await db.rollback()
        raise server_error_exc