import hashlib
import json
from collections import OrderedDict
from threading import Lock
from typing import Any

from pydantic import BaseModel

from app.core.settings import settings


class LLMResponseCache:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self._items: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._lock = Lock()

    def get(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            value = self._items.get(key)
            if value is None:
                return None

            self._items.move_to_end(key)
            return value

    def set(self, key: str, value: BaseModel) -> None:
        if self.max_size <= 0:
            return

        with self._lock:
            self._items[key] = value.model_dump(mode="json")
            self._items.move_to_end(key)

            while len(self._items) > self.max_size:
                self._items.popitem(last=False)


llm_response_cache = LLMResponseCache(settings.LLM_CACHE_MAX_SIZE)


def build_llm_cache_key(
    chain_name: str,
    model_name: str,
    prompt_version: str,
    llm_input: BaseModel,
) -> str:
    payload = {
        "chain_name": chain_name,
        "model_name": model_name,
        "prompt_version": prompt_version,
        "input": llm_input.model_dump(mode="json"),
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"{chain_name}:{model_name}:{prompt_version}:{digest}"
