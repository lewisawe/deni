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
from .data_pack import get_forum, get_lender, get_product, load_pack

# USSD-friendly short product menu (subset for the small screen).
USSD_PRODUCTS = [
    ("M-KOPA phone", "mkopa-x10-phone"),
    ("Watu boda", "watu-boda"),
    ("App loan 1000/30d", "quickcash-30d"),
]


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
        return "END Product not found."
    b = compute_cost(_offer(p))
    lender = get_lender(country, p["lender_id"]) or {}
    lic = lender.get("cbk_dcp_licensed")
    if lic is False:
        lic_line = "NOT on CBK licensed list. May not be able to legally chase you."
    elif lic is True:
        lic_line = "Licensed by CBK."
    else:
        lic_line = "Not a CBK digital lender."
    return (
        f"END {p['label']}\n"
        f"Pay KES {b.total_paid} for KES {b.principal}\n"
        f"= {b.markup_pct}% more (APR {b.apr_pct}%)\n"
        f"{lic_line}\n"
        f"Deni: know before you borrow."
    )


def _check_lender(country: str, name: str) -> str:
    name_l = name.strip().lower()
    for ld in load_pack(country)["lenders"]["lenders"]:
        if name_l and name_l in ld["name"].lower():
            lic = ld.get("cbk_dcp_licensed")
            if lic is True:
                return f"END {ld['name']}: Licensed by CBK."
            if lic is False:
                return (f"END {ld['name']}: NOT on CBK licensed list. "
                        f"An unlicensed lender may not legally enforce repayment.")
            return f"END {ld['name']}: not a CBK digital lender. {ld.get('regime','')}"
    return "END Lender not found in Deni's list. Check CBK's licensed DCP register."


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
    law = s.get("law_statement", "")[:200]
    return (
        f"END {s['title'][:40]}\n"
        f"{law}\n"
        f"Go to: {forum.get('name', 'the relevant body')}\n"
        f"Not legal advice."
    )
