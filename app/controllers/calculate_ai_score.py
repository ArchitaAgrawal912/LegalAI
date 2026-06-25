import traceback
import asyncio
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.precedent import PrecedentCase
from app.models.precedent import PrecedentCase
from app import crud
from app.errors import user_not_found_exc, server_error_exc, case_not_found_exc
from app.schemas.precedent import PrecedentScoreResult
from app.models.legal_case import LegalCase
from app.services.legal_service import LegalAnalysisService

import asyncio # <--- Make sure this is at the top of your file!

async def calculate_ai_scores_controller(case_id: UUID, db: AsyncSession, legal_service: LegalAnalysisService):
    try:
        # 1. Fetch the main case to get the facts
        db_case = await crud.legal_case.get(db, id=case_id)
        if not db_case:
            raise case_not_found_exc()

        # 2. Fetch ONLY precedents belonging to THIS case that are unscored
        query = select(PrecedentCase).where(
            PrecedentCase.case_id == case_id
        )
        result = await db.execute(query)
        unscored_precedents = result.scalars().all()

        if unscored_precedents:
            print(f"🎯 Found {len(unscored_precedents)} unscored precedents for case {case_id}")
            
            # 3. Score them using Groq with rate-limit protection
            for precedent in unscored_precedents:
                snippet_to_send = getattr(precedent, 'snippet', "Snippet not available.")
                
                score_data = await legal_service.score_precedent_relevance(
                    case_summary=db_case.lawyer_approved_summary or db_case.raw_description,
                    precedent_title=precedent.title,
                    precedent_snippet=snippet_to_send
                )

                precedent.ai_score = score_data.score
                db.add(precedent)

                # Pause for 1.5 seconds to prevent the Groq "0 score" rate limit block!
                await asyncio.sleep(1.5) 

            # Save all scores to the database
            await db.commit()

        # 4. Fetch ALL precedents for THIS specific case to return to the frontend
        final_query = select(PrecedentCase).where(PrecedentCase.case_id == case_id)
        final_result = await db.execute(final_query)
        all_case_precedents = final_result.scalars().all()

        updated_precedents = [
            {
                "id": p.id,
                "title": p.title,
                "doc_id": p.doc_id,
                "doc_url": p.doc_url,
                "ai_score": p.ai_score
            } for p in all_case_precedents
        ]

        return {
            "message": f"Successfully scored {len(unscored_precedents)} precedents.",
            "scored_precedents": updated_precedents
        }

    except Exception as e:
        await db.rollback()
        print("🚨 CRITICAL ERROR DURING AI SCORING 🚨")
        traceback.print_exc()
        raise server_error_exc(e)