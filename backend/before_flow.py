"""The BEFORE flow (Deni R1,R3,R4,R5,R7,R13): given a product or a raw offer,
return true cost + licence status + what's at risk + a cheaper licensed alternative,
each with sources. Money math is deterministic (cost_engine); this only assembles."""
from __future__ import annotations

from decimal import Decimal

from .cost_engine import CostBreakdown, LoanOffer, compute_cost
from .data_pack import get_lender, get_product, licence_authority, load_pack

SECURITY_RISK = {
    "device-lock": "Miss a payment and the device is locked remotely until you clear arrears.",
    "repossession-tracker": "The asset has a tracker and can be repossessed on default. Repossession without proper notice and lawful process has been ruled unlawful by Kenyan courts.",
    "collateral-joint-registration": "Secured on an asset registered in the lender's joint name, and often group-guaranteed: a fellow member's default can expose your asset.",
    "none": "No asset security. Note: harassment and contact-scraping are documented collection tactics by rogue apps — that has its own recourse.",
}


def _offer_from_product(p: dict) -> LoanOffer:
    kw = dict(
        principal=Decimal(str(p["principal"])),
        term_days=int(p["term_days"]),
        deposit=Decimal(str(p.get("deposit", 0))),
        instalment_amount=Decimal(str(p.get("instalment_amount", 0))),
        instalment_frequency=p.get("instalment_frequency", "monthly"),
        num_instalments=int(p.get("num_instalments", 0)),
        extra_fees=Decimal(str(p.get("extra_fees", 0))),
    )
    if p.get("repay_total") is not None:
        kw["repay_total"] = Decimal(str(p["repay_total"]))
    return LoanOffer(**kw)


def _breakdown_dict(b: CostBreakdown) -> dict:
    return {
        "principal": str(b.principal),
        "total_paid": str(b.total_paid),
        "total_cost": str(b.total_cost),
        "markup_pct": str(b.markup_pct),
        "apr_pct": str(b.apr_pct),
        "term_days": b.term_days,
        "steps": b.steps,
    }


def _licence_view(country: str, lender: dict) -> dict:
    la = licence_authority(country)
    licensed = lender.get(la["field"])
    if licensed is True:
        status = "licensed"
        note = f"{la['registered_label']}. {lender['name']} {la['registered_note']}"
    elif licensed is False:
        status = "unlicensed"
        note = f"{lender['name']} {la['unregistered_note']}"
    else:
        status = "not-applicable"
        note = f"{lender['name']}: {lender.get('regime', la['not_applicable_note'])}"
    return {
        "status": status,
        "note": note,
        "findings": lender.get("findings", []),
    }


def cheaper_alternative(country: str, product: dict) -> dict | None:
    """Find a cheaper LICENSED/REGISTERED product in the same category (R5)."""
    field = licence_authority(country)["field"]
    this_cost = compute_cost(_offer_from_product(product))
    best = None
    for p in load_pack(country)["products"]["products"]:
        if p["id"] == product["id"] or p["category"] != product["category"]:
            continue
        lender = get_lender(country, p["lender_id"]) or {}
        if lender.get(field) is not True:
            continue
        b = compute_cost(_offer_from_product(p))
        if b.apr_pct < this_cost.apr_pct and (best is None or b.apr_pct < best[1].apr_pct):
            best = (p, b)
    if not best:
        return None
    p, b = best
    return {"product_id": p["id"], "label": p["label"], "cost": _breakdown_dict(b)}


def evaluate_product(country: str, product_id: str) -> dict:
    """Full BEFORE assessment for a known product."""
    product = get_product(country, product_id)
    if not product:
        raise ValueError(f"unknown product '{product_id}'")
    lender = get_lender(country, product["lender_id"]) or {}
    cost = compute_cost(_offer_from_product(product))
    return {
        "product": {"id": product["id"], "label": product["label"],
                    "category": product["category"], "lender": lender.get("name")},
        "cost": _breakdown_dict(cost),
        "licence": _licence_view(country, lender),
        "at_risk": {
            "security_type": product.get("security_type", "none"),
            "note": product.get("security_note")
                    or SECURITY_RISK.get(product.get("security_type", "none")),
        },
        "alternative": cheaper_alternative(country, product),
        "sources": product.get("sources", []),
        "data_date": load_pack(country)["products"]["_meta"].get("last_updated"),
        "disclaimer": "Figures computed from the shown inputs. Not financial or legal advice.",
    }


def evaluate_offer(principal, term_days, *, repay_total=None, deposit=0,
                   instalment_amount=0, instalment_frequency="monthly",
                   num_instalments=0, extra_fees=0) -> dict:
    """BEFORE assessment for a raw offer (no known product/lender)."""
    kw = dict(principal=Decimal(str(principal)), term_days=int(term_days),
              deposit=Decimal(str(deposit)),
              instalment_amount=Decimal(str(instalment_amount)),
              instalment_frequency=instalment_frequency,
              num_instalments=int(num_instalments),
              extra_fees=Decimal(str(extra_fees)))
    if repay_total is not None:
        kw["repay_total"] = Decimal(str(repay_total))
    return {"cost": _breakdown_dict(compute_cost(LoanOffer(**kw))),
            "disclaimer": "Figures computed from the inputs you gave. Not financial or legal advice."}
