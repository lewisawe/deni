"""AI-assisted parse (SMS/screenshot -> offer fields) and explain (multilingual),
Deni R2 + R11. The model extracts and phrases; it never computes the cost."""
from __future__ import annotations

from . import ai

LANG_NAME = {"en": "English", "sw": "Kiswahili", "sheng": "Sheng (Kenyan urban slang)"}

_PARSE_SYSTEM = (
    "You extract loan-offer fields from a Kenyan lender's SMS or screenshot. "
    "Return JSON with keys: principal (number, amount received or cash price), "
    "repay_total (number or null, single lump repayment), deposit (number), "
    "instalment_amount (number), instalment_frequency (one of daily|weekly|biweekly|"
    "monthly|lump), num_instalments (integer), term_days (integer), "
    "extra_fees (number), lender_name (string or null), confidence (0-1). "
    "Use null/0 when unknown. Never invent numbers not present."
)

_REQUIRED = {"principal", "term_days"}


def parse_offer(text: str = "", image_bytes: bytes | None = None,
                image_format: str = "png") -> dict:
    """Extract offer fields for user confirmation (R2). Never auto-proceeds."""
    if not ai.available():
        return {"available": False,
                "reason": "AI parsing unavailable — enter the numbers manually."}
    prompt = text or "Extract the loan offer from the attached image."
    try:
        data = ai.converse_json(ai.MODEL_LITE, _PARSE_SYSTEM, prompt,
                                image_bytes=image_bytes, image_format=image_format)
    except Exception as exc:  # noqa: BLE001 — degrade, don't crash a demo
        return {"available": False, "reason": f"Could not parse: {exc}"}

    fields = {
        "principal": data.get("principal") or 0,
        "repay_total": data.get("repay_total"),
        "deposit": data.get("deposit") or 0,
        "instalment_amount": data.get("instalment_amount") or 0,
        "instalment_frequency": data.get("instalment_frequency") or "monthly",
        "num_instalments": data.get("num_instalments") or 0,
        "term_days": data.get("term_days") or 0,
        "extra_fees": data.get("extra_fees") or 0,
        "lender_name": data.get("lender_name"),
    }
    # Guard against double-counting: a lump repay_total already includes any fee/interest.
    # If the model also reported extra_fees, it has likely split the same money out — drop it.
    if fields["repay_total"]:
        fields["extra_fees"] = 0
    missing = [k for k in _REQUIRED if not fields.get(k)]
    return {
        "available": True,
        "fields": fields,
        "confidence": data.get("confidence", 0.5),
        "needs_confirmation": True,  # always confirm before compute (R2)
        "missing": missing,
    }


_EXPLAIN_SYSTEM = (
    "You are Deni, explaining a loan's true cost to a Kenyan borrower in plain, warm, "
    "clear {lang}. You are given the already-computed figures — DO NOT recompute or "
    "change any number. Explain in 2-3 short sentences what the numbers mean and why "
    "it matters. Keep it simple for someone stressed and not financially trained. "
    "Do not give legal advice."
)


def explain_cost(cost: dict, lang: str = "en") -> dict:
    """Phrase the computed cost in the chosen language (R11). Numbers come from code."""
    lang_name = LANG_NAME.get(lang, "English")
    if not ai.available():
        return {"available": False, "text": None}
    facts = (f"APR {cost['apr_pct']}%, total paid KES {cost['total_paid']}, "
             f"value received KES {cost['principal']}, markup {cost['markup_pct']}%, "
             f"term {cost['term_days']} days.")
    try:
        text = ai.converse(ai.MODEL_LITE,
                           _EXPLAIN_SYSTEM.format(lang=lang_name), facts,
                           max_tokens=250, temperature=0.4)
        return {"available": True, "text": text, "lang": lang}
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "text": None, "reason": str(exc)}
