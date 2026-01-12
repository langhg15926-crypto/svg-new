import base64
import json
import os
from typing import Optional

import requests

from .provider_config import load_provider_config

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"


def _load_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as handle:
        return base64.b64encode(handle.read()).decode("utf-8")


def call_ai_to_json(
    image_path: str,
    prompt_text: str,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout_s: Optional[int] = None,
) -> str:
    """
    Calls an OpenAI-compatible chat/completions endpoint.

    Priority:
    1) Function arguments
    2) Environment variables: AI_BASE_URL, AI_API_KEY, AI_MODEL, AI_TIMEOUT_S
    3) config/provider.json
    4) Built-in defaults
    """
    config = load_provider_config()
    base_url = (
        base_url
        or os.getenv("AI_BASE_URL")
        or config.get("base_url")
        or DEFAULT_BASE_URL
    ).rstrip("/")
    api_key = api_key or os.getenv("AI_API_KEY") or config.get("api_key")
    model = model or os.getenv("AI_MODEL") or config.get("model") or DEFAULT_MODEL
    timeout_s = timeout_s or int(os.getenv("AI_TIMEOUT_S", config.get("timeout_s", 120)))

    if not api_key:
        raise RuntimeError(
            "Missing API key. Set AI_API_KEY, pass api_key, or configure config/provider.json."
        )

    image_b64 = _load_image_base64(image_path)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a meticulous vector redraw assistant.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            },
        ],
        "temperature": 0,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{base_url}/chat/completions",
        headers=headers,
        data=json.dumps(payload),
        timeout=timeout_s,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Unexpected response format from AI provider.") from exc
