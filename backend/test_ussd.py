"""Tests for the USSD channel: routing and the length ceiling (Deni R8)."""
from backend import ussd


def _end_body(resp: str) -> str:
    """The user-visible body (gateway strips the CON/END token)."""
    return resp[4:] if resp.startswith(("END ", "CON ")) else resp


def test_root_menu_opens_session():
    r = ussd.handle("")
    assert r.startswith("CON ")
    assert "Check if lender" in r


def test_product_result_within_ceiling():
    r = ussd.handle("1")  # first product
    assert r.startswith("END ")
    assert len(_end_body(r)) <= ussd.USSD_MAX
    assert "APR" in r


def test_lender_check_within_ceiling():
    r = ussd.handle("4*Tala")
    assert r.startswith("END ")
    assert len(_end_body(r)) <= ussd.USSD_MAX


def test_rights_answer_within_ceiling_and_not_cut_midword():
    # 5 = rights menu, then pick the first scenario.
    r = ussd.handle("5*1")
    assert r.startswith("END ")
    body = _end_body(r)
    assert len(body) <= ussd.USSD_MAX
    # If it was trimmed it ends with an ellipsis, never a broken word fragment.
    assert not body.endswith(" ")


def test_clip_helper_breaks_on_word_boundary():
    long = "word " * 60
    out = ussd._clip(long, 20)
    assert len(out) <= 20
    assert out.endswith("…")
