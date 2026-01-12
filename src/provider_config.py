import json
from pathlib import Path
from typing import Any, Dict

from .config import BASE


DEFAULT_CONFIG = {
    "base_url": "https://api.openai.com/v1",
    "api_key": "",
    "model": "gpt-4o-mini",
    "timeout_s": 120,
}


def load_provider_config() -> Dict[str, Any]:
    config_path = BASE / "config" / "provider.json"
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()

    with open(config_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    merged = DEFAULT_CONFIG.copy()
    merged.update({k: v for k, v in data.items() if v is not None})
    return merged
