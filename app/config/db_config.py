# app/config/db_config.py
import os
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

# Centralized Database URL strictly from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Security Check: Agar .env me URL nahi mili toh server start hone se pehle error de dega
if not DATABASE_URL:
    raise ValueError("🚨 DATABASE_URL is missing! Please check your .env file.")