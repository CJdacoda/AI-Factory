from __future__ import annotations

from typing import Any, Dict, List, Optional

from litellm import completion as _litellm_completion

# Allowed provider blocks (drop Grok entirely).
GEMINI_FLASH_MODEL = "gemini/gemini-2.5-flash"
MISTRAL_LARGE_MODEL = "mistral/mistral-large-latest"


def _validate_allowed_model(model_name: str) -> None:
    # Hard stop to prevent accidental Grok re-introduction.
    if "grok" in model_name.lower():
        raise ValueError(f"Disallowed model reference detected: {model_name}")


def gemini_flash_completion(messages: List[Dict[str, Any]], **kwargs: Any) -> Any:
    """Thin wrapper forcing LiteLLM requests through Gemini Flash only."""
    _validate_allowed_model(GEMINI_FLASH_MODEL)
    return _litellm_completion(model=GEMINI_FLASH_MODEL, messages=messages, **kwargs)


def mistral_large_completion(
    messages: List[Dict[str, Any]], **kwargs: Any
) -> Any:
    """Thin wrapper forcing LiteLLM requests through Mistral Large only."""
    _validate_allowed_model(MISTRAL_LARGE_MODEL)
    return _litellm_completion(model=MISTRAL_LARGE_MODEL, messages=messages, **kwargs)

