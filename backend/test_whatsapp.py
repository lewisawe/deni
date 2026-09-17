"""Tests for the WhatsApp conversational engine (paste-loan and describe-problem)."""
from backend import whatsapp


def test_greeting_returns_menu():
    r = whatsapp.handle_message("+254700", "hi")
    assert "Deni" in r and "1." in r


def test_pasted_loan_confirms_then_returns_true_cost():
    """R2: WhatsApp echoes the figures and waits for confirmation before pricing."""
    prompt = whatsapp.handle_message("+254701", "you qualify for 1000 repay 1150 in 30 days")
    assert "1150" in prompt and "YES" in prompt          # confirmation prompt first
    assert "APR" not in prompt                             # not computed yet
    result = whatsapp.handle_message("+254701", "YES")     # confirm
    assert "182.5% APR" in result
    assert "True cost" in result


def test_numeric_shorthand_loan():
    prompt = whatsapp.handle_message("+254702", "1000, 1150, 30")
    assert "YES" in prompt
    result = whatsapp.handle_message("+254702", "yes")
    assert "182.5% APR" in result


def test_corrected_numbers_replace_pending_offer():
    """Sending new numbers instead of YES re-parses rather than computing the old ones."""
    whatsapp.handle_message("+254777", "1000, 1150, 30")
    prompt = whatsapp.handle_message("+254777", "2000, 2600, 60")
    assert "2600" in prompt and "YES" in prompt
    result = whatsapp.handle_message("+254777", "YES")
    assert "APR" in result


def test_problem_with_numbers_routes_to_recourse_not_calculator():
    """A report that happens to contain numbers must go to recourse, not pricing."""
    r = whatsapp.handle_message("+254704", "they took my bike and I still owe 5000 over 3 months")
    assert "APR" not in r                                  # not treated as a loan to price
    assert ("prepared complaint" in r.lower()) or ("Where to go" in r) or ("repossess" in r.lower())


def test_described_problem_returns_law_and_complaint():
    r = whatsapp.handle_message("+254703", "they are calling my contacts to shame me")
    assert "prepared complaint" in r.lower()
    assert "Data Protection" in r  # law read from the KE pack


def test_south_africa_routes_to_sa_bodies():
    r = whatsapp.handle_message("+27820000000", "they are calling my contacts", country="za")
    assert ("Information Regulator" in r) or ("NCR" in r)
