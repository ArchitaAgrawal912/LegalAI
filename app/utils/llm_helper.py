import logging
import time
import json

from groq import Groq
from app.core.config import GROQ_API_KEY
from app.core.logger import logger

client = Groq(api_key=GROQ_API_KEY)



def call_llm(
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        retries: int = 3
):
    for attempt in range(retries):

        try:
            logger.info(
                f"LLM Call attempt {attempt+1} using {model}"
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt 
                    } 
                ]
            )

            result = response.choices[0].message.content.strip()

            result = (
                result.replace("```json", "").replace("```", "")
            )

            logger.info("LLM Success")

            return json.loads(result)
        
        except Exception as e:
            logger.error(f"LLM failed : {e}")

            if attempt == retries - 1:
                raise Exception("LLM failed after retries")
            
            time.sleep(2)