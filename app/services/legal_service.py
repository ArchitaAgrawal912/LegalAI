import logging
import json
from groq import AsyncGroq
from app.core.config import settings
from app.schemas.case import CaseResponse, DraftResponse
from app.schemas.section import LegalSection
from app.decorators import with_api_retry
from app.schemas.precedent import PrecedentScoreResult

# 🚨 NEW: Import your prompt functions
from app.prompts.legal_analysis import (
    get_draft_summary_prompt,
    get_charge_extraction_prompt,
)

logger = logging.getLogger(__name__)


class LegalAnalysisService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model_id = "llama-3.3-70b-versatile"
        schema_instructions = CaseResponse.model_json_schema()

    @with_api_retry
    async def draft_summary(self, case_description: str) -> DraftResponse:
        """PHASE 1: Reads the raw input and generates a clean title and summary."""

        # 🚨 NEW: Generate the prompt using the imported function
        prompt = get_draft_summary_prompt(case_description)

        response = await self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_id,
            response_format={"type": "json_object"},
        )

        result_dict = json.loads(response.choices[0].message.content)
        return DraftResponse(**result_dict)

    @with_api_retry
    async def extract_charges(self, approved_summary: str) -> list[LegalSection]:
        """PHASE 2: Takes the HUMAN-VERIFIED summary and extracts penal charges."""

        # 🚨 NEW: Generate the prompt using the imported function
        prompt = get_charge_extraction_prompt(approved_summary)

        response = await self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_id,
            response_format={"type": "json_object"},
        )

        result_dict = json.loads(response.choices[0].message.content)
        return [LegalSection(**charge) for charge in result_dict.get("charges", [])]


    async def score_precedent_relevance(self, case_summary: str, precedent_title: str, precedent_snippet: str) -> PrecedentScoreResult:
        """
        Uses Groq (Llama 3.1) with Chain-of-Thought prompting and a strict rubric 
        to accurately score the relevance of a Kanoon case.
        """
        prompt = f"""
        You are an expert Indian Supreme Court legal analyst. 
        Evaluate the relevance of a retrieved precedent case against the current case facts.

        CURRENT CASE FACTS:
        {case_summary}

        PRECEDENT TITLE: {precedent_title}
        PRECEDENT SNIPPET: {precedent_snippet}

        SCORING RUBRIC:
        - 0.8 to 1.0: Highly Relevant (Matches the core facts, exact IPC sections, or primary legal question).
        - 0.4 to 0.7: Moderately Relevant (Shares some minor facts or general legal principles, but the core context differs).
        - 0.0 to 0.3: Irrelevant (Completely different crime, unrelated context, or the snippet contains no useful facts).

        Respond ONLY with a valid JSON object matching this exact schema:
        {{
            "analysis": "<Write 2 sentences comparing the facts and charges step-by-step>",
            "score": <float between 0.0 and 1.0 based on the rubric>,
            "reasoning": "<One brief summary sentence justifying the final score>"
        }}
        {{
            "score": <float between 0.0 and 1.0>,
            "reasoning": "<one sentence explaining the score>"
        }}
        """

        print(f"🧠 Asking Groq to score precedent: {precedent_title}...")
        
        try:
            response = await self.client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You output strict JSON. Never use markdown formatting."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            raw_response = response.choices[0].message.content
            print(f"🔍 Raw Groq Output: {raw_response}") # <-- THIS WILL SHOW US WHAT GROQ IS DOING
            
            # Bulletproof JSON parsing: strip out markdown blocks if the AI misbehaves
            clean_json = raw_response.replace("```json", "").replace("```", "").strip()
            
            parsed_data = json.loads(clean_json)
            
            # Ensure the score is actually a float before Pydantic reads it
            return PrecedentScoreResult(
                score=float(parsed_data.get("score", 0.0)),
                reasoning=str(parsed_data.get("reasoning", "No reasoning provided."))
            )
            
        except Exception as e:
            # THIS will tell us exactly why it failed in your terminal!
            print(f"⚠️ FAILED TO SCORE '{precedent_title}'. ERROR: {str(e)}") 
            return PrecedentScoreResult(score=0.0, reasoning=f"Failed to calculate AI score: {str(e)}")