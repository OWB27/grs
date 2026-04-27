from pathlib import Path
import os

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


def _get_int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError:
        return default


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_RERANK_MODEL: str = os.getenv("OPENAI_RERANK_MODEL", "gpt-5.4-mini")
    OPENAI_RERANK_ENABLED: bool = os.getenv("OPENAI_RERANK_ENABLED", "false").lower() == "true"
    OPENAI_RERANK_TIMEOUT_SECONDS: int = _get_int_env("OPENAI_RERANK_TIMEOUT_SECONDS", 20)
    OPENAI_RERANK_MAX_RETRIES: int = _get_int_env("OPENAI_RERANK_MAX_RETRIES", 2)


settings = Settings()
