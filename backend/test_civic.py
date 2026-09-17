"""Tests for the civic-hardening layer: findings split, positive-regime framing,
and the recourse no-match safety floor. These protect the trust claims that a judge
or a named lender would probe hardest."""
from backend import data_pack as d
from backend import recourse as r


def test_findings_split_official_vs_reported():
    """A regulator/court action and a press report must be kept separate, so a news
    article is never presented as an official finding."""
    mogo = d.check_lender("ke", "Mogo")
    assert "official_findings" in mogo and "reported_concerns" in mogo
    assert any("CAK" in f.get("body", "") for f in mogo["official_findings"])
    # The press repossession item is a reported concern, not an official finding.
    assert all("CAK" not in f.get("body", "") for f in mogo["reported_concerns"])


def test_not_applicable_leads_with_regime_not_absence():
    """A regulated asset financier must not read as 'unlicensed'; the result leads
    with the regime it IS regulated under."""
    mogo = d.check_lender("ke", "Mogo")
    assert mogo["status"] == "not-applicable"
    assert "different regime" in mogo["label"].lower()
    assert "financier" in mogo["note"].lower()


def test_unmatched_problem_returns_safety_net():
    """Never dead-end: an unmatched problem still returns general bodies to contact."""
    res = r.recourse("someone in my village keeps insulting me at the market", "en", "ke")
    assert res["matched"] is False
    bodies = res.get("safety_net", {}).get("bodies", [])
    assert len(bodies) >= 3
    assert any("Police" in b["name"] for b in bodies)
    assert all(b.get("contact") for b in bodies)


def test_safety_net_is_country_specific():
    za = r.recourse("some unrelated civic problem", "en", "za")
    names = [b["name"] for b in za.get("safety_net", {}).get("bodies", [])]
    assert any("SAPS" in n or "Information Regulator" in n for n in names)


def test_matched_scenario_has_no_safety_net_noise():
    res = r.recourse("they are calling my contacts to shame me", "en", "ke")
    assert res["matched"] is True
    assert "law_statement" in res
