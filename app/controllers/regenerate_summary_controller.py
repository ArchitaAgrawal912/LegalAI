import traceback
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.errors import server_error_exc
from app.models.user import User
from app.services.legal_service import LegalAnalysisService


async def regenerate_summary_controller(
    case_id: UUID,
    new_description: str,
    current_user: User,
    db: AsyncSession,
    legal_service: LegalAnalysisService,
):
    try:
        # 1. Fetch the existing case
        db_case = await crud.legal_case.get(db, id=case_id)

        if not db_case:
            return None

        # 2. Verify ownership
        if db_case.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to modify this case.",
            )

        # 3. Call Groq ONLY for the updated summary and title
        print(f"🚀 Calling Groq to Regenerate Summary for Case {case_id}...")

        draft_result = await legal_service.draft_summary(
            case_description=new_description
        )

        # 4. Overwrite the existing data
        db_case.raw_description = new_description
        db_case.title = draft_result.title
        db_case.llm_summary = draft_result.summary
        db_case.status = "pending_review"

        await db.commit()
        await db.refresh(db_case)

        return db_case

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR IN REGENERATE PHASE 🚨")
        traceback.print_exc()
        raise server_error_exc(e)