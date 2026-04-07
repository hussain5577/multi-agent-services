# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Change GOOGLE_API_KEY to GEMINI_API_KEY to match your .env
    GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()
    DEFAULT_MODEL = "llama-3.3-70b-versatile"

settings = Settings()