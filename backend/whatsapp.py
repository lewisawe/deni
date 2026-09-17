"""WhatsApp channel (Deni R8): a richer conversational surface than USSD.

A provider (Twilio, Meta Cloud API, or Africa's Talking WhatsApp) POSTs each inbound
message to a webhook; we reply with text. Unlike USSD (menu-only, ~182 chars), WhatsApp
allows free text and long replies, so this engine does more than the USSD menu:

  - a numbered menu for structured navigation (shared idea with USSD);
  - "paste a loan": if the message looks like a loan offer, parse it and reply with the
    true cost + licence view;
  - "describe a problem": if the message describes harassment/repossession/etc., reply
    with the law + the public body + the prepared complaint text.

HONESTY: going live needs an approved WhatsApp Business number (provider + Meta
verification). This webhook is real and works against a provider's SANDBOX (e.g. the
Twilio WhatsApp sandbox) exactly as it would in production.
"""
from __future__ import annotations

import re
from decimal import Decimal

from . import recourse as recourse_mod
from . import ussd
from .cost_engine import LoanOffer, compute_cost
from .data_pack import currency, licence_authority

# sender -> conversational state (in-memory; fine for a demo, no long-term PII).
_SESSIONS: dict[str, dict] = {}
_RESET_WORDS = {"hi", "hello", "menu", "start", "deni", "restart", "0"}
_CONFIRM_WORDS = {"yes", "y", "ndio", "ndiyo", "sawa", "eeh", "confirm", "compute"}

_MENU = (
    "*Deni*: know your rights as a borrower.\n\n"
    "Reply with:\n"
    "1. Check a loan's true cost (paste the lender's SMS)\n"
    "2. Check if a lender is licensed (type its name)\n"
    "3. Know your rights / take action (describe your problem)\n\n"
    "Or just paste a loan SMS, or describe what's happening, any time."
)


def handle_message(sender: str, message: str, country: str = "ke") -> str:
    """Handle one inbound WhatsApp message; return the reply text."""
    msg = (message or "").strip()
    low = msg.lower()
    st = _SESSIONS.setdefault(sender, {"mode": None})

    if low in _RESET_WORDS:
        _SESSIONS[sender] = {"mode": None}
        return _MENU

    # A pending loan is awaiting confirmation: YES computes it, new numbers replace it,
    # anything else cancels. Mirrors the web app's confirm-before-compute step (R2).
    if st.get("pending_offer"):
        if low in _CONFIRM_WORDS:
            offer = st.pop("pending_offer")
            st["mode"] = None
            return _compute_offer(country, offer)
        if _nums(msg):  # user re-sent corrected numbers
            return _cost_reply(country, msg)
        st.pop("pending_offer", None)
        st["mode"] = None
        # fall through and re-interpret the message below

    # Explicit menu choices set a mode; otherwise we infer intent from the text.
    if msg == "1":
        st["mode"] = "cost"
        return "Paste the loan SMS the lender sent you (or type: amount, repay, days).\nExample: 1000, 1150, 30"
    if msg == "2":
        st["mode"] = "lender"
        return f"Type the lender's name ({licence_authority(country)['examples']})."
    if msg == "3":
        st["mode"] = "rights"
        return "Describe what's happening (e.g. 'they are calling my contacts', 'they took my bike', 'I want a refund')."

    # Mode-directed handling.
    if st.get("mode") == "lender":
        st["mode"] = None
        return _lender_reply(country, msg)
    if st.get("mode") == "rights":
        st["mode"] = None
        return _recourse_reply(country, msg)
    if st.get("mode") == "cost":
        st["mode"] = None
        return _cost_reply(country, msg, sender)

    # No mode: infer intent from the message itself. A problem description wins over
    # the numeric heuristic, because a report like "they took my bike, I owe 5000"
    # carries numbers but is not a loan to price.
    if _looks_like_problem(low):
        return _recourse_reply(country, msg)
    if _looks_like_loan(msg):
        return _cost_reply(country, msg, sender)

    # Fallback: show the menu.
    return _MENU


# ---------- intent detection ----------
_PROBLEM_WORDS = ("harass", "calling", "contact", "shame", "threaten", "repossess",
                  "took my", "take my", "seize", "bike", "boda", "crb", "blacklist",
                  "listed", "refund", "owe me", "overpaid", "mislead", "unlicensed")


def _looks_like_loan(msg: str) -> bool:
    # Two or more numbers present suggests a loan offer (amount/repay/term).
    nums = re.findall(r"\d[\d,]*", msg)
    return len(nums) >= 2


def _looks_like_problem(low: str) -> bool:
    return any(w in low for w in _PROBLEM_WORDS)


# ---------- replies ----------
def _nums(msg: str) -> list[int]:
    return [int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", msg)]


def _cost_reply(country: str, msg: str, sender: str = "") -> str:
    """Parse a pasted loan and ask the user to confirm the figures BEFORE computing.

    The web app shows parsed fields and waits for confirmation (R2); WhatsApp mirrors
    that here instead of silently pricing whatever numbers it grabbed. The parsed offer
    is held in the session; a YES computes it, corrected numbers replace it."""
    nums = _nums(msg)
    if len(nums) >= 3:
        principal, repay, days = nums[0], nums[1], nums[2]
    elif len(nums) == 2:
        principal, repay, days = nums[0], nums[1], 30
    else:
        return ("I couldn't read the numbers. Send it as: amount, repay, days.\n"
                "Example: 1000, 1150, 30")
    if repay < principal:
        return ("I read the amount received as larger than the repayment, which can't "
                "be right. Send it as: amount received, total repaid, days.\n"
                "Example: 1000, 1150, 30")
    cur = currency(country)["symbol"]
    offer = {"principal": principal, "repay": repay, "days": days}
    if sender:
        _SESSIONS.setdefault(sender, {"mode": None})["pending_offer"] = offer
    days_note = "" if len(nums) >= 3 else " (assuming 30 days, send the term if different)"
    return (
        f"Let me check I read this right:\n"
        f"• Amount received: {cur} {principal}\n"
        f"• Total to repay: {cur} {repay}\n"
        f"• Term: {days} days{days_note}\n\n"
        f"Reply *YES* to see the true cost, or send the correct numbers as "
        f"amount, repay, days."
    )


def _compute_offer(country: str, offer: dict) -> str:
    """Compute and format a confirmed offer (the second half of the R2 flow)."""
    cur = currency(country)["symbol"]
    try:
        b = compute_cost(LoanOffer(principal=Decimal(offer["principal"]),
                                   term_days=int(offer["days"]),
                                   repay_total=Decimal(offer["repay"])))
    except Exception:  # noqa: BLE001
        return "Those numbers didn't compute. Send: amount, repay, days (e.g. 1000, 1150, 30)."
    return (
        f"*True cost*\n"
        f"You pay {cur} {b.total_paid} for {cur} {b.principal}.\n"
        f"That's {b.markup_pct}% more. *{b.apr_pct}% APR*.\n\n"
        f"{b.steps[-1]}\n\n"
        f"Reply 2 to check if the lender is licensed, or 3 to know your rights. "
        f"Not financial or legal advice."
    )


def _lender_reply(country: str, name: str) -> str:
    from .data_pack import check_lender
    r = check_lender(country, name)
    lines = [f"*{r['label']}*", r.get("note", "")]
    for f in (r.get("findings") or [])[:2]:
        lines.append(f"\n• {f.get('body','')} ({f.get('date','')}): {f.get('summary','')}")
    lines.append("\nReply 3 to take action, or 'menu'. Facts only, each sourced.")
    return "\n".join(x for x in lines if x)


def _recourse_reply(country: str, text: str) -> str:
    r = recourse_mod.recourse(text, "en", country)
    if not r.get("matched"):
        return (r.get("message") or "Couldn't match that. Describe what the lender is "
                "doing (e.g. calling your contacts, taking your bike, wrong CRB listing).")
    forums = r.get("forums") or ([{"name": r["forum"]["name"]}] if r.get("forum") else [])
    forum_names = ", ".join(f["name"] for f in forums)
    out = [
        f"*{r.get('title','')}*",
        r.get("law_statement", ""),
        f"\n_{r.get('condition','')}_" if r.get("condition") else "",
        f"\n*Where to go:* {forum_names}" if forum_names else "",
    ]
    if r.get("complaint"):
        out.append(f"\n*Your prepared complaint* (case {r.get('case_ref','')}):\n\n{r['complaint']}")
    out.append("\nEdit the details in [brackets] and send it to the body above. Not legal advice.")
    return "\n".join(x for x in out if x)
