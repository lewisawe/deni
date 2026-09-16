"""Deterministic loan cost engine (Deni R1).

The trust core. NO AI touches these numbers. Every figure is computed here and the
arithmetic is exposed so the UI can show the working. Money is handled in KES using
Decimal to avoid float error.

Definitions used:
- principal:   amount the borrower actually receives (cash loan) OR cash price of a
               financed asset (device/bike/car), i.e. the value obtained today.
- total_paid:  everything the borrower pays: deposit + all instalments + fees.
- total_cost:  total_paid - principal (the true cost of the credit).
- APR:         annualised percentage rate, simple annualisation of the period rate:
                 period_rate = total_cost / principal over the loan term,
                 APR = period_rate * (365 / term_days) * 100.
               (Simple/nominal APR, transparent and easy to show. Documented, not a
               hidden reducing-balance figure.)
- markup_pct:  total_cost / principal * 100 (headline "you pay X% more than cash").
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP

FREQ_DAYS = {"daily": 1, "weekly": 7, "biweekly": 14, "monthly": 30}


def _money(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _pct(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


@dataclass
class LoanOffer:
    """Inputs describing a credit offer. Amounts in KES."""
    principal: Decimal              # cash received or cash price of the asset
    term_days: int                  # total loan duration in days
    deposit: Decimal = Decimal("0")
    instalment_amount: Decimal = Decimal("0")
    instalment_frequency: str = "monthly"  # daily|weekly|biweekly|monthly|lump
    num_instalments: int = 0
    extra_fees: Decimal = Decimal("0")     # one-off fees not in instalments
    # For a single lump repayment (typical app loan): set repay_total instead.
    repay_total: Decimal | None = None


@dataclass
class CostBreakdown:
    """Computed result + the arithmetic used (R1: show the working)."""
    principal: Decimal
    total_paid: Decimal
    total_cost: Decimal
    markup_pct: Decimal
    apr_pct: Decimal
    term_days: int
    steps: list[str] = field(default_factory=list)


def compute_cost(offer: LoanOffer) -> CostBreakdown:
    """Compute true cost, markup and APR for a loan offer. Deterministic."""
    principal = Decimal(str(offer.principal))
    if principal <= 0:
        raise ValueError("principal must be > 0")
    if offer.term_days <= 0:
        raise ValueError("term_days must be > 0")

    steps: list[str] = []

    if offer.repay_total is not None:
        # Lump-sum repayment (e.g. app cash loan).
        total_paid = Decimal(str(offer.repay_total)) + Decimal(str(offer.extra_fees))
        steps.append(
            f"Total to repay = {_money(offer.repay_total)}"
            + (f" + fees {_money(offer.extra_fees)}" if offer.extra_fees else "")
            + f" = {_money(total_paid)}"
        )
    else:
        instalments_total = Decimal(str(offer.instalment_amount)) * offer.num_instalments
        total_paid = (
            Decimal(str(offer.deposit))
            + instalments_total
            + Decimal(str(offer.extra_fees))
        )
        parts = []
        if offer.deposit:
            parts.append(f"deposit {_money(offer.deposit)}")
        if offer.num_instalments:
            parts.append(
                f"{offer.num_instalments} x {_money(offer.instalment_amount)} "
                f"({offer.instalment_frequency}) = {_money(instalments_total)}"
            )
        if offer.extra_fees:
            parts.append(f"fees {_money(offer.extra_fees)}")
        steps.append("Total paid = " + " + ".join(parts) + f" = {_money(total_paid)}")

    total_cost = total_paid - principal
    steps.append(
        f"True cost of credit = total paid {_money(total_paid)} - "
        f"value received {_money(principal)} = {_money(total_cost)}"
    )

    markup_pct = (total_cost / principal) * Decimal("100")
    steps.append(
        f"Markup = {_money(total_cost)} / {_money(principal)} x 100 = {_pct(markup_pct)}%"
    )

    apr_pct = markup_pct * (Decimal("365") / Decimal(offer.term_days))
    steps.append(
        f"APR = {_pct(markup_pct)}% x (365 / {offer.term_days} days) = {_pct(apr_pct)}%"
    )

    return CostBreakdown(
        principal=_money(principal),
        total_paid=_money(total_paid),
        total_cost=_money(total_cost),
        markup_pct=_pct(markup_pct),
        apr_pct=_pct(apr_pct),
        term_days=offer.term_days,
        steps=steps,
    )
