from pathlib import Path
import os

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


def _get_env(name: str, default: str | None = None, fallback_name: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is not None:
        return value

    if fallback_name is not None:
        return os.getenv(fallback_name, default)

    return default


def _get_bool_env(name: str, default: bool, fallback_name: str | None = None) -> bool:
    raw_value = _get_env(name, fallback_name=fallback_name)
    if raw_value is None:
        return default

    return raw_value.lower() == "true"


def _get_int_env(name: str, default: int, fallback_name: str | None = None) -> int:
    raw_value = _get_env(name, fallback_name=fallback_name)
    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError:
        return default


class Settings:
    LLM_API_KEY: str | None = _get_env("LLM_API_KEY", fallback_name="OPENAI_API_KEY")
    LLM_RERANK_MODEL: str = _get_env("LLM_RERANK_MODEL", "gpt-5.4-nano", "OPENAI_RERANK_MODEL")
    LLM_RERANK_ENABLED: bool = _get_bool_env("LLM_RERANK_ENABLED", False, "OPENAI_RERANK_ENABLED")
    LLM_RERANK_TIMEOUT_SECONDS: int = _get_int_env(
        "LLM_RERANK_TIMEOUT_SECONDS",
        20,
        "OPENAI_RERANK_TIMEOUT_SECONDS",
    )
    LLM_RERANK_MAX_RETRIES: int = _get_int_env(
        "LLM_RERANK_MAX_RETRIES",
        2,
        "OPENAI_RERANK_MAX_RETRIES",
    )
    LLM_RERANK_CANDIDATE_COUNT: int = _get_int_env("LLM_RERANK_CANDIDATE_COUNT", 6)
    LLM_PROFILE_TAG_COUNT: int = _get_int_env("LLM_PROFILE_TAG_COUNT", 5)
    LLM_MATCHED_TAG_COUNT: int = _get_int_env("LLM_MATCHED_TAG_COUNT", 3)
    LLM_CACHE_ENABLED: bool = _get_bool_env("LLM_CACHE_ENABLED", False)
    LLM_CACHE_MAX_SIZE: int = _get_int_env("LLM_CACHE_MAX_SIZE", 128)
    ENABLE_RECOMMEND_DIAGNOSTICS: bool = _get_bool_env("ENABLE_RECOMMEND_DIAGNOSTICS", False)


settings = Settings()
