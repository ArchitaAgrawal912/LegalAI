# app/config/ai_config.py

import os
from google.genai import types
from dotenv import load_dotenv
from app.config.aws_secrets import get_secret

# Load environment variables cleanly
load_dotenv()

# Configuration for Gemini API models and parameters
GEMINI_MODEL = 'gemini-2.5-flash'

# Your exact AWS Secret Name matching your IAM/Secrets Manager console
AWS_SECRET_NAME = "LegalAI_configurations"

# Centralized Generation Configuration for Structured JSON Output
AI_GENERATION_CONFIG = types.GenerateContentConfig(
    response_mime_type="application/json",
)

def get_gemini_api_key() -> str:
    """
    Attempts to fetch the Gemini API key from AWS Secrets Manager first.
    Falls back to local .env if AWS credentials are not configured or fail.
    """
    # FIX: String "AWS_SECRET_NAME" ke badle direct variable use kiya 👍
    aws_secrets = get_secret(AWS_SECRET_NAME)
    
    if aws_secrets and "GEMINI_API_KEY" in aws_secrets:
        return aws_secrets["GEMINI_API_KEY"]
    
    # Fallback to local environment variable if AWS fails/is not setup locally
    return os.getenv("GEMINI_API_KEY")


def get_indian_kanoon_api_key() -> str:
    """
    Fetches Indian Kanoon token from AWS Secrets Manager or falls back to .env
    """
    aws_secrets = get_secret(AWS_SECRET_NAME)
    if aws_secrets and "INDIAN_KANOON_API_KEY" in aws_secrets:
        return aws_secrets["INDIAN_KANOON_API_KEY"]
    return os.getenv("INDIAN_KANOON_API_KEY")