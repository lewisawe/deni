"""Tests for server-side redaction (Deni Track 3 anonymity + R10 privacy).
Every channel (including WhatsApp, which sends raw text) must strip identifying
data before the problem is classified or used."""
from backend.recourse import redact


def test_redacts_phone_id_email_name():
    txt, hits = redact(
        "My name is John Mwangi, ID 12345678, call 0712345678 or john@x.com"
    )
    assert "John Mwangi" not in txt
    assert "12345678" not in txt
    assert "0712345678" not in txt
    assert "john@x.com" not in txt
    assert set(hits) >= {"phone number", "ID number", "email", "name"}


def test_keeps_the_shape_of_the_problem():
    """Redaction must not destroy the words that let us classify the scenario."""
    txt, hits = redact("they are calling everyone in my phonebook and shaming me")
    assert "calling" in txt and "phonebook" in txt
    assert hits == []


def test_idempotent_when_already_redacted():
    """The web app redacts on-device; re-running server-side must not double-mangle."""
    once, _ = redact("call me on 0712345678")
    twice, hits = redact(once)
    assert once == twice
    assert hits == []
