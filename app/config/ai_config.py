# app/config/ai_config.py

from google.genai import types
from app.prompts.legal_prompts import SYSTEM_PROMPT

# Configuration for Gemini API models and parameters
GEMINI_MODEL = 'gemini-2.5-flash'

# Centralized Generation Configuration
AI_GENERATION_CONFIG = types.GenerateContentConfig(
    response_mime_type="application/json",
)

def format_legal_analysis_contents(case_text: str) -> str:
    """
    Stitches the system prompt and user data into a single string.
    Centralizing this prevents hardcoding template strings in the controller.
    """
    return f"System Instructions:\n{SYSTEM_PROMPT}\n\nUser Case Data:\nAnalyze this case: {case_text}"