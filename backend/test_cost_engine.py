"""Tests for the deterministic cost engine (Deni R1). The number is the whole pitch —
it must be provably correct."""
from decimal import Decimal

import pytest

from backend.cost_engine import LoanOffer, compute_cost


def test_app_loan_lump_sum():
    """Borrow 1,000, repay 1,150 in 30 days.
    cost=150, markup=15%, APR = 15% * 365/30 = 182.5%."""
    r = compute_cost(LoanOffer(principal=Decimal("1000"), term_days=30,
                               repay_total=Decimal("1150")))
    assert r.total_cost == Decimal("150.00")
    assert r.markup_pct == Decimal("15.0")
    assert r.apr_pct == Decimal("182.5")
    assert any("365" in s for s in r.steps)  # working is shown


def test_app_loan_with_fee():
    """Borrow 1,000, repay 1,150 + 50 fee in 30 days. cost=200, markup=20%."""
    r = compute_cost(LoanOffer(principal=Decimal("1000"), term_days=30,
                               repay_total=Decimal("1150"), extra_fees=Decimal("50")))
    assert r.total_paid == Decimal("1200.00")
    assert r.total_cost == Decimal("200.00")
    assert r.markup_pct == Decimal("20.0")


def test_payg_device_daily():
    """PAYG phone: cash price 12,000; deposit 2,000 + 60/day for 365 days.
    total = 2000 + 21900 = 23900; cost = 11900; markup ~99.2%."""
    r = compute_cost(LoanOffer(
        principal=Decimal("12000"), term_days=365,
        deposit=Decimal("2000"),
        instalment_amount=Decimal("60"), instalment_frequency="daily",
        num_instalments=365,
    ))
    assert r.total_paid == Decimal("23900.00")
    assert r.total_cost == Decimal("11900.00")
    assert r.markup_pct == Decimal("99.2")
    # APR = 99.2 * 365/365 = 99.2%
    assert r.apr_pct == Decimal("99.2")


def test_moto_weekly():
    """Boda bike: cash 180,000; deposit 30,000 + 3,500/week for 104 weeks (2yr).
    total = 30000 + 364000 = 394000; cost = 214000; markup ~118.9%."""
    r = compute_cost(LoanOffer(
        principal=Decimal("180000"), term_days=728,
        deposit=Decimal("30000"),
        instalment_amount=Decimal("3500"), instalment_frequency="weekly",
        num_instalments=104,
    ))
    assert r.total_paid == Decimal("394000.00")
    assert r.total_cost == Decimal("214000.00")
    assert r.markup_pct == Decimal("118.9")


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        compute_cost(LoanOffer(principal=Decimal("0"), term_days=30,
                               repay_total=Decimal("100")))
    with pytest.raises(ValueError):
        compute_cost(LoanOffer(principal=Decimal("1000"), term_days=0,
                               repay_total=Decimal("1100")))


def test_working_is_exposed():
    """R1: the arithmetic must be shown, not just the result."""
    r = compute_cost(LoanOffer(principal=Decimal("1000"), term_days=30,
                               repay_total=Decimal("1150")))
    assert len(r.steps) >= 3
    assert any("True cost" in s for s in r.steps)
