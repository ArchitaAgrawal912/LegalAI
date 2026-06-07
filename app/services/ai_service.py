import requests
import json
import time

from app.core.config import settings
from app.core.logger import logger

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def generate_case_summary(case_text: str):

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a senior Indian legal expert with deep knowledge of both IPC (Indian Penal Code) and BNS (Bharatiya Nyaya Sanhita 2023).

Analyze the following case description and identify ALL applicable IPC and BNS sections.

VERY IMPORTANT - SUB-SECTIONS RULE:
Many IPC sections have lettered or numbered sub-parts. You MUST include all relevant sub-parts as separate entries. Examples:
- Section 354 has sub-parts: 354A (sexual harassment), 354B (assault to disrobe), 354C (voyeurism), 354D (stalking)
- Section 376 has sub-parts: 376A, 376B, 376C, 376D, 376E
- Section 498 has sub-part: 498A (cruelty by husband)
- Section 304 has sub-parts: 304A (death by negligence), 304B (dowry death)
- Section 326 has sub-parts: 326A (acid attack), 326B (attempt acid attack)
- BNS sections also have sub-parts like BNS 64(2), BNS 316(2), BNS 74 etc.

Return MINIMUM 4 and MAXIMUM 12 entries including all relevant sub-parts.

OTHER RULES:
- For BNS sections use prefix "BNS " (e.g. "BNS 316", "BNS 64(2)")
- For IPC sub-parts use letter suffix (e.g. "354A", "304B", "498A")
- For numbered sub-clauses use bracket (e.g. "376(2)", "307(1)")
- Each sub-part must be a SEPARATE entry with its own title, punishment and reason
- Return ONLY valid JSON, no markdown, no extra text

Return in this exact format:
{{
  "sections": [
    {{
      "section_code": "354D",
      "title": "Stalking",
      "punishment": "First conviction: up to 3 years, Second conviction: up to 5 years",
      "reason": "Accused repeatedly followed and contacted the victim despite her objection"
    }},
    {{
      "section_code": "354A",
      "title": "Sexual Harassment",
      "punishment": "Up to 3 years imprisonment or fine or both",
      "reason": "Accused made unwelcome physical contact and sexual advances towards victim"
    }},
    {{
      "section_code": "BNS 74",
      "title": "Assault on woman with intent to outrage modesty (BNS)",
      "punishment": "Up to 5 years imprisonment and fine",
      "reason": "BNS equivalent applicable for assault on woman in this case"
    }},
    {{
      "section_code": "498A",
      "title": "Cruelty by Husband or Relatives",
      "punishment": "Up to 3 years imprisonment and fine",
      "reason": "Victim subjected to cruelty and harassment by husband"
    }}
  ]
}}

Case Description:
{case_text}
"""

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    # Retry mechanism
    for attempt in range(1, MAX_RETRIES + 1):

        try:
            logger.info(f"LLM CALL | generate_case_summary | attempt={attempt}")

            response = requests.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            data = response.json()

            logger.info(f"LLM RESPONSE | status={response.status_code}")

            content = data["choices"][0]["message"]["content"]

            logger.info(f"LLM CONTENT RECEIVED | length={len(content)}")

            # Strip markdown code blocks if LLM wraps response
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            parsed = json.loads(content.strip())

            logger.info(f"LLM PARSE SUCCESS | sections_count={len(parsed.get('sections', []))}")

            return parsed

        except Exception as e:
            logger.error(f"LLM CALL FAILED | attempt={attempt} | error={str(e)}")

            if attempt < MAX_RETRIES:
                logger.info(f"RETRYING in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("ALL RETRIES EXHAUSTED | returning empty sections")
                return {"sections": []}