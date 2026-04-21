from pathlib import Path
import os

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_RERANK_MODEL: str = os.getenv("OPENAI_RERANK_MODEL", "gpt-5.4-mini")
    OPENAI_RERANK_ENABLED: bool = os.getenv("OPENAI_RERANK_ENABLED", "false").lower() == "true"


settings = Settings()