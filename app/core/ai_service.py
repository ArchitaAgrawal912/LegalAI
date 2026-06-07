# app/core/ai_service.py

from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
import logging
from app.config.ai_config import get_gemini_api_key, GEMINI_MODEL


logger = logging.getLogger("api_logger")



@retry(
    stop=stop_after_attempt(3),          
    wait=wait_exponential(multiplier=1, min=2, max=10), 
    reraise=True                         
)
def call_gemini_llm(prompt_content: str) -> str:
    """
    Universal LLM Caller: Sends prompt to Gemini, handles retries, 
    and returns a clean, markdown-free string.
    """
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        raise Exception("Gemini API Key missing")
        
    ai_client = genai.Client(api_key=gemini_key)
    
    # AI Call
    response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_content
    )
    
    # 🎯 BULLETPROOF CLEANUP
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return raw_text