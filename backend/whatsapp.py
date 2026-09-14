"""WhatsApp channel (Deni R8) — same idea as USSD.

A WhatsApp provider (Africa's Talking WhatsApp, Meta Cloud API, or Twilio) POSTs each
inbound message to a webhook; we reply with text. WhatsApp is turn-based (no persistent
USSD session), so we keep a tiny per-sender state and feed the SAME stateless USSD menu
engine by reconstructing the accumulated 'text' path. One engine, two channels.

HONESTY: going live needs an approved WhatsApp Business number (provider + Meta
verification), not obtainable in the sprint. This webhook is real and works against a
simulated provider POST — the same way USSD is demoed on the Africa's Talking simulator.
"""
from __future__ import annotations

from . import ussd

# sender -> list of accumulated menu choices (in-memory; fine for demo, no PII stored long-term)
_SESSIONS: dict[str, list[str]] = {}
_RESET_WORDS = {"hi", "hello", "menu", "start", "deni", "restart", "0"}


def handle_message(sender: str, message: str) -> str:
    """Handle one inbound WhatsApp message; return the reply text."""
    msg = (message or "").strip()
    low = msg.lower()

    # greeting / reset -> fresh menu
    if low in _RESET_WORDS or sender not in _SESSIONS:
        _SESSIONS[sender] = []
        return _to_whatsapp(ussd.handle(""))

    path = _SESSIONS[sender]
    path.append(msg)
    reply = ussd.handle("*".join(path))

    # If the engine ended the session (END), reset so the next message starts over.
    if reply.startswith("END"):
        _SESSIONS[sender] = []
    return _to_whatsapp(reply)


def _to_whatsapp(ussd_reply: str) -> str:
    """Turn a USSD CON/END reply into a natural WhatsApp message."""
    body = ussd_reply[3:].strip() if ussd_reply[:3] in ("CON", "END") else ussd_reply
    if ussd_reply.startswith("CON"):
        body += "\n\n(Reply with a number. Send 'menu' to restart.)"
    else:
        body += "\n\nSend 'menu' to check another loan."
    return body
