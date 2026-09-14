"""AWS Bedrock (Amazon Nova) client for Deni.

Guardrails (specs/design.md):
- AI never computes money or states law. It only parses offers, translates, and
  phrases explanations, and fills fixed templates.
- Graceful degradation: if Bedrock is unreachable, callers get a clear
  `available=False` result rather than a crash, so the deterministic core (cost
  engine, licence check) keeps working in a demo.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

# Verified working IDs (see specs/design.md): Nova 2 needs the us. inference profile.
MODEL_LITE = os.getenv("DENI_MODEL_LITE", "us.amazon.nova-2-lite-v1:0")
MODEL_PRO = os.getenv("DENI_MODEL_PRO", "us.amazon.nova-pro-v1:0")
REGION = os.getenv("AWS_REGION", "us-east-1")


@lru_cache(maxsize=1)
def _client():
    import boto3  # imported lazily so the app runs without boto3 configured
    return boto3.client("bedrock-runtime", region_name=REGION)


def available() -> bool:
    """Best-effort check that a Bedrock client can be constructed."""
    try:
        _client()
        return True
    except Exception:
        return False


def converse(model_id: str, system: str, user_text: str,
             *, image_bytes: bytes | None = None, image_format: str = "png",
             max_tokens: int = 800, temperature: float = 0.2) -> str:
    """Single-turn Converse call. Returns the model's text, or raises."""
    content: list[dict] = [{"text": user_text}]
    if image_bytes is not None:
        content.append({"image": {"format": image_format,
                                  "source": {"bytes": image_bytes}}})
    resp = _client().converse(
        modelId=model_id,
        system=[{"text": system}],
        messages=[{"role": "user", "content": content}],
        inferenceConfig={"maxTokens": max_tokens, "temperature": temperature},
    )
    return resp["output"]["message"]["content"][0]["text"].strip()


def converse_json(model_id: str, system: str, user_text: str, **kw) -> dict:
    """Converse and parse a JSON object from the reply (tolerant of code fences)."""
    raw = converse(model_id, system + "\nRespond with ONLY a JSON object.",
                   user_text, **kw)
    txt = raw.strip()
    if txt.startswith("```"):
        txt = txt.split("```", 2)[1].lstrip("json").strip()
        if txt.endswith("```"):
            txt = txt[:-3].strip()
    start, end = txt.find("{"), txt.rfind("}")
    if start != -1 and end != -1:
        txt = txt[start:end + 1]
    return json.loads(txt)
