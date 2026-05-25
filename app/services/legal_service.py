import logging
import json
from groq import AsyncGroq
from app.core.config import settings
from app.models.schemas import CaseResponse

logger = logging.getLogger(__name__)

class LegalAnalysisService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model_id = "llama-3.3-70b-versatile"
        
        schema_instructions = CaseResponse.model_json_schema()
        
        self.system_instruction = (
            "You are an expert Indian criminal lawyer. Analyze the provided case facts and "
            "determine all applicable charges under the Indian Penal Code (IPC). For every IPC "
            "section identified, accurately map the corresponding section under the new "
            "Bharatiya Nyaya Sanhita (BNS). Rely strictly on the provided text; do not invent facts. "
            "You MUST respond ONLY in valid JSON that perfectly matches this schema: "
            f"{json.dumps(schema_instructions)}"
        )

    async def analyze_case(self, case_description: str) -> CaseResponse:
        try:
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": f"Analyze the following incident facts: {case_description}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            raw_json = response.choices[0].message.content
            
            if not raw_json:
                raise ValueError("Received an empty response from Groq.")
                
            return CaseResponse.model_validate_json(raw_json)
            
        except Exception as e:
            logger.error(f"Groq AI Analysis Error: {e}", exc_info=True)
            raise Exception("Failed to perform legal analysis due to an internal AI error.")