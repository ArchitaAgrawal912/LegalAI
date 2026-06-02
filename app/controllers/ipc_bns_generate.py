import json
from google import genai
from app.config.ai_config import get_gemini_api_key, GEMINI_MODEL
from app.prompts.legal_prompts import format_judge_prompt

def generate_charges_from_llm(approved_summary: str) -> dict:
    """Takes approved summary, calls Gemini, and returns IPC/BNS sections dict."""
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        raise Exception("Gemini API Key missing")
        
    ai_client = genai.Client(api_key=gemini_key)
    prompt_content = format_judge_prompt(approved_summary)
    
    response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_content
    )
    
    # 🎯 BULLETPROOF JSON CLEANUP
    raw_text = response.text.strip()
    # Replace function har jagah se markdown hata dega, chahe space ho ya na ho
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
    
    return json.loads(raw_text)