from dotenv import load_dotenv
import os

load_dotenv()

import os
from dataclasses import dataclass


@dataclass
class Settings:
    #  API KEYS
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")


    #  MODELS 
    TEXT_MODEL_NAME = "llama-3.3-70b-versatile"
    SMALL_TEXT_MODEL_NAME = "llama-3.1-8b-instant"
    ITT_MODEL_NAME: str = "llama-3.2-11b-vision-preview"
    TTI_MODEL_NAME: str = "black-forest-labs/FLUX.1-schnell"
    TTS_MODEL_NAME: str = "eleven_multilingual_v2"

    #  MEMORY (Qdrant)
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    MEMORY_TOP_K: int = 5

    #  CONVERSATION CONTROL
    ROUTER_MESSAGES_TO_ANALYZE: int = 5
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 20
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 10

    #  SHORT TERM MEMORY (SQLite)
    SHORT_TERM_MEMORY_DB_PATH: str = "sqlite:///./short_term_memory.db"

DEBUG = bool = False
settings = Settings()