import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
INDIAN_KANOON_API_KEY = os.getenv("INDIAN_KANOON_API_KEY")

