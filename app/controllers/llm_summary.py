import json
from google import genai
from app.config.ai_config import get_gemini_api_key, GEMINI_MODEL
from app.prompts.llm_summary import format_summarizer_prompt

def generate_summary_from_llm(raw_description: str) -> dict:
    """Takes raw text, calls Gemini, and returns a JSON dictionary with title and summary."""
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        raise Exception("Gemini API Key missing")
        
    ai_client = genai.Client(api_key=gemini_key)
    prompt_content = format_summarizer_prompt(raw_description)
    
    response = ai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_content
    )
    
    # LLM ke text ko clean JSON mein convert karna
    raw_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(raw_text)