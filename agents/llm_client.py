"""
agents/llm_client.py

Single call-site every agent goes through instead of instantiating a
provider SDK directly. Swap providers with one env var (LLM_PROVIDER)
instead of editing diagnosis_agent.py / roadmap_agent.py /
verification_agent.py.

Supported providers:
    groq      - free tier, no credit card required (default)
    gemini    - Google AI Studio free tier, no credit card required
    anthropic - paid; only a small one-time trial credit, no ongoing
                free tier, so it's opt-in rather than the default here
"""

import logging
from typing import Optional

from . import config

logger = logging.getLogger(__name__)


class LLMUnavailable(Exception):
    """Raised when the configured provider has no API key set, or the
    provider name itself is unrecognized. Callers should catch this the
    same way they'd catch a missing ANTHROPIC_API_KEY before — treat it
    as "fall back to rule-based logic", not a hard error."""


def is_configured() -> bool:
    """Whether the currently selected LLM_PROVIDER has credentials set."""
    provider = config.LLM_PROVIDER
    if provider == "groq":
        return bool(config.GROQ_API_KEY)
    if provider == "gemini":
        return bool(config.GEMINI_API_KEY)
    if provider == "anthropic":
        return bool(config.ANTHROPIC_API_KEY)
    return False


def complete(system: str, user_content: str, max_tokens: int = 1024) -> str:
    """Runs a single system+user turn against the configured provider and
    returns the raw text response. Raises LLMUnavailable if no key is set
    for the selected provider, or requests.RequestException-family errors
    on network/API failures — callers already wrap these in their own
    try/except and fall back to rule-based logic."""
    provider = config.LLM_PROVIDER

    if provider == "groq":
        return _complete_groq(system, user_content, max_tokens)
    if provider == "gemini":
        return _complete_gemini(system, user_content, max_tokens)
    if provider == "anthropic":
        return _complete_anthropic(system, user_content, max_tokens)

    raise LLMUnavailable(f"Unknown LLM_PROVIDER: {provider!r}")


def _complete_groq(system: str, user_content: str, max_tokens: int) -> str:
    if not config.GROQ_API_KEY:
        raise LLMUnavailable("GROQ_API_KEY not set")

    import requests

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.GROQ_MODEL,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _complete_gemini(system: str, user_content: str, max_tokens: int) -> str:
    if not config.GEMINI_API_KEY:
        raise LLMUnavailable("GEMINI_API_KEY not set")

    import requests

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{config.GEMINI_MODEL}:generateContent?key={config.GEMINI_API_KEY}"
    )
    resp = requests.post(
        url,
        json={
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user_content}]}],
            "generationConfig": {"maxOutputTokens": max_tokens},
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _complete_anthropic(system: str, user_content: str, max_tokens: int) -> str:
    if not config.ANTHROPIC_API_KEY:
        raise LLMUnavailable("ANTHROPIC_API_KEY not set")

    from anthropic import Anthropic

    client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text
