"""Tests for the WhatsApp conversational engine (paste-loan and describe-problem)."""
from backend import whatsapp


def test_greeting_returns_menu():
    r = whatsapp.handle_message("+254700", "hi")
    assert "Deni" in r and "1." in r


def test_pasted_loan_returns_true_cost():
    r = whatsapp.handle_message("+254701", "you qualify for 1000 repay 1150 in 30 days")
    assert "182.5% APR" in r
    assert "True cost" in r


def test_numeric_shorthand_loan():
    r = whatsapp.handle_message("+254702", "1000, 1150, 30")
    assert "182.5% APR" in r


def test_described_problem_returns_law_and_complaint():
    r = whatsapp.handle_message("+254703", "they are calling my contacts to shame me")
    assert "prepared complaint" in r.lower()
    assert "Data Protection" in r  # law read from the KE pack


def test_south_africa_routes_to_sa_bodies():
    r = whatsapp.handle_message("+27820000000", "they are calling my contacts", country="za")
    assert ("Information Regulator" in r) or ("NCR" in r)
