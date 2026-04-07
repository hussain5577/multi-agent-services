# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Change GOOGLE_API_KEY to GEMINI_API_KEY to match your .env
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY").strip()
    DEFAULT_MODEL = "gemini-3-flash-preview"

settings = Settings()