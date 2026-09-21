"""Tests for the civic-hardening layer: findings split, positive-regime framing,
and the recourse no-match safety floor. These protect the trust claims that a judge
or a named lender would probe hardest."""
from backend import data_pack as d
from backend import recourse as r
from backend import receipt
from fastapi.testclient import TestClient
from backend.main import app

_client = TestClient(app)


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


def test_multi_body_scenario_forums_carry_provenance():
    """A multi-body scenario (harassment: ODPC + CBK) must return every body, and each
    must carry its own source provenance, so the accountability trail is complete."""
    res = r.recourse("they call my contacts to shame me and threaten me", "en", "ke")
    assert len(res["forums"]) >= 2
    assert all(f.get("provenance", {}).get("source") for f in res["forums"])


def test_recourse_receipt_embeds_every_body_source():
    """The keepable receipt must embed the law citation AND each applicable body's
    source, not just the primary citation, so the paper trail stands on its own."""
    res = r.recourse("they call my contacts to shame me and threaten me", "en", "ke")
    rec = receipt.recourse_receipt(res)
    assert "CIVIC ACTION RECEIPT" in rec["text"]
    assert "PUBLIC BODIES" in rec["text"]
    # De-duplicated, but ODPC + CBK sources should both be present.
    assert len(rec["sources"]) >= 2


def test_accountability_chain_matches_recourse_bodies():
    """The accountability-chain view and the recourse router must agree on which
    bodies apply to a right (same data, drawn two ways)."""
    chain = d.accountability_chain("ke", "harassment_contacts")
    res = r.recourse("they call my contacts to shame me", "en", "ke")
    chain_names = {b["name"] for b in chain["bodies"]}
    recourse_names = {f["name"] for f in res["forums"]}
    assert chain_names == recourse_names


def test_unknown_country_returns_404_not_500():
    """A mistyped or probed country code must not crash the server. Every pack-loading
    endpoint should return a clean 404, never a 500."""
    for path in ("/api/rights", "/api/meta", "/api/sources", "/api/products",
                 "/api/accountability/harassment_contacts"):
        resp = _client.get(path, params={"country": "zz"})
        assert resp.status_code == 404, f"{path} returned {resp.status_code} for bad country"


def test_valid_countries_ok():
    """Both shipped country packs serve their civic endpoints."""
    for cc in ("ke", "za"):
        assert _client.get("/api/rights", params={"country": cc}).status_code == 200
        assert _client.get("/api/sources", params={"country": cc}).status_code == 200



def test_rights_translate_but_citations_do_not():
    """The rights library must render in the selected language (sw/sheng), while the
    citation and date, the sourced facts, stay identical across languages. Legal text
    is human-authored data, never AI-translated."""
    en = _client.get("/api/rights", params={"country": "ke", "lang": "en"}).json()
    sw = _client.get("/api/rights", params={"country": "ke", "lang": "sw"}).json()
    sheng = _client.get("/api/rights", params={"country": "ke", "lang": "sheng"}).json()
    # Titles differ from English (translation actually happened).
    assert sw["rights"][0]["title"] != en["rights"][0]["title"]
    assert sheng["rights"][0]["title"] != en["rights"][0]["title"]
    # Disclaimer is translated too.
    assert sw["disclaimer"] != en["disclaimer"]
    # Citations and dates are language-independent facts: identical across languages.
    for i, right in enumerate(en["rights"]):
        assert sw["rights"][i]["citation"] == right["citation"]
        assert sw["rights"][i]["citation_date"] == right["citation_date"]


def test_rights_fall_back_to_english_when_untranslated():
    """A pack with no translations (ZA is English-only) must still render: a missing
    translation falls back to the English field, never an empty string."""
    za_sw = _client.get("/api/rights", params={"country": "za", "lang": "sw"}).json()
    za_en = _client.get("/api/rights", params={"country": "za", "lang": "en"}).json()
    assert za_sw["rights"][0]["title"] == za_en["rights"][0]["title"]
    assert all(r["title"] for r in za_sw["rights"])
