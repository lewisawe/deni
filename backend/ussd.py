"""USSD channel (Deni R8): Africa's Talking gateway.

AT is stateless: each keypress POSTs the FULL accumulated input (e.g. "1*2*3").
We reply with a plain-text body: "CON ..." keeps the session open, "END ..."
closes it. This engine reuses the deterministic cost engine and licence data, so a
basic phone with no internet or app gets the true-cost + licence check.

Menu tree:
  (root)                -> choose a loan category / demo product
   1 M-KOPA phone       -> END: true cost + markup + what's at risk
   2 Watu boda          -> END: ...
   3 App loan (unlic.)  -> END: cost + NOT licensed warning
   4 Check a lender     -> CON: type name -> END: licensed / not
"""
from __future__ import annotations

from decimal import Decimal

from .cost_engine import LoanOffer, compute_cost
from .data_pack import get_forum, get_lender, get_product, licence_authority, load_pack

# USSD-friendly short product menu (subset for the small screen).
USSD_PRODUCTS = [
    ("M-KOPA phone", "mkopa-x10-phone"),
    ("Watu boda", "watu-boda"),
    ("App loan 1000/30d", "quickcash-30d"),
]

# USSD gateways cap a single response body (commonly ~160-182 chars). We keep END
# screens within a safe ceiling so a long product label or legal statement is never
# cut mid-word by the gateway.
USSD_MAX = 160


def _clip(text: str, limit: int = USSD_MAX) -> str:
    """Trim to `limit` chars without breaking a word; add an ellipsis if trimmed."""
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip() + "…"


def _end(body: str) -> str:
    """Format an END response, clipping the body under the USSD ceiling.

    The 'END ' prefix is a protocol token the gateway strips, so the ceiling applies
    to the message the user actually sees (the body)."""
    return "END " + _clip(body)


def _offer(p: dict) -> LoanOffer:
    kw = dict(principal=Decimal(str(p["principal"])), term_days=int(p["term_days"]),
              deposit=Decimal(str(p.get("deposit", 0))),
              instalment_amount=Decimal(str(p.get("instalment_amount", 0))),
              instalment_frequency=p.get("instalment_frequency", "monthly"),
              num_instalments=int(p.get("num_instalments", 0)),
              extra_fees=Decimal(str(p.get("extra_fees", 0))))
    if p.get("repay_total") is not None:
        kw["repay_total"] = Decimal(str(p["repay_total"]))
    return LoanOffer(**kw)


def _product_result(country: str, product_id: str) -> str:
    p = get_product(country, product_id)
    if not p:
        return _end("Product not found.")
    b = compute_cost(_offer(p))
    lender = get_lender(country, p["lender_id"]) or {}
    la = licence_authority(country)
    field = la["field"]
    cur = load_pack(country)["products"].get("_meta", {}).get("currency", {}).get("symbol", "KES")
    lic = lender.get(field)
    auth = la["authority_short"]
    if lic is False:
        lic_line = f"NOT registered with {auth}. May not be able to legally chase you."
    elif lic is True:
        lic_line = f"Registered with {auth}."
    else:
        lic_line = f"Not a {auth}-listed lender."
    return _end(
        f"{p['label']}\n"
        f"Pay {cur} {b.total_paid} for {cur} {b.principal}\n"
        f"= {b.markup_pct}% more (APR {b.apr_pct}%)\n"
        f"{lic_line}\n"
        f"Deni: know before you borrow."
    )


def _check_lender(country: str, name: str) -> str:
    la = licence_authority(country)
    field = la["field"]
    auth = la["authority_short"]
    name_l = name.strip().lower()
    for ld in load_pack(country)["lenders"]["lenders"]:
        if name_l and name_l in ld["name"].lower():
            lic = ld.get(field)
            if lic is True:
                return _end(f"{ld['name']}: Registered with {auth}.")
            if lic is False:
                return _end(f"{ld['name']}: NOT registered with {auth}. "
                            f"An unregistered lender may not legally enforce repayment.")
            return _end(f"{ld['name']}: not a {auth}-listed lender. {ld.get('regime','')}")
    return _end(f"Lender not found in Deni's list. Check the {auth} register.")


def handle(text: str, country: str = "ke") -> str:
    """Route an Africa's Talking USSD request. `text` is the accumulated input."""
    parts = [p for p in (text or "").split("*") if p != ""]

    if not parts:  # root menu
        menu = "\n".join(f"{i+1}. {label}" for i, (label, _) in enumerate(USSD_PRODUCTS))
        return (f"CON Deni - know your rights\n{menu}\n"
                f"4. Check if lender is licensed\n5. Know your rights")

    choice = parts[0]
    if choice in ("1", "2", "3"):
        idx = int(choice) - 1
        if idx < len(USSD_PRODUCTS):
            return _product_result(country, USSD_PRODUCTS[idx][1])
        return "END Invalid choice."

    if choice == "4":
        if len(parts) < 2:
            return "CON Type the lender name (e.g. Tala, QuickCash, Mogo):"
        return _check_lender(country, parts[1])

    if choice == "5":
        return _rights_menu(country, parts[1:])

    return "END Invalid choice. Dial again."


def _rights_menu(country: str, rest: list[str]) -> str:
    """USSD know-your-rights: list scenarios, then show law + forum for one.
    Brings the civic 'access to information' feature to a basic phone."""
    scenarios = load_pack(country)["rules"]["scenarios"]
    if not rest:
        lines = "\n".join(f"{i+1}. {s['title'][:34]}" for i, s in enumerate(scenarios))
        return f"CON Know your rights - pick one:\n{lines}"
    try:
        idx = int(rest[0]) - 1
    except ValueError:
        return "END Invalid choice."
    if not (0 <= idx < len(scenarios)):
        return "END Invalid choice."
    s = scenarios[idx]
    forum = get_forum(country, s.get("forum_key", "")) or {}
    # Build the body, then let _end() clip to the USSD ceiling as a whole so we never
    # cut mid-word. Reserve room for the title + forum line by trimming the law text.
    law = s.get("law_statement", "")
    title = s["title"][:40]
    forum_line = f"Go to: {forum.get('name', 'the relevant body')}"
    fixed = f"{title}\n\n{forum_line}\nNot legal advice."
    room = max(0, USSD_MAX - len(fixed) - 2)
    law = _clip(law, room) if room else ""
    return _end(f"{title}\n{law}\n{forum_line}\nNot legal advice.")
