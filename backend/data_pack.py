"""Loads a per-country data pack (Deni R12: scalability is a data swap)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@lru_cache(maxsize=8)
def load_pack(country: str = "ke") -> dict:
    """Load and cache a country's data pack (lenders, products, rules, forums, templates)."""
    base = DATA_DIR / country.lower()
    if not base.is_dir():
        raise FileNotFoundError(f"No data pack for country '{country}'")
    pack = {}
    for name in ("lenders", "products", "rules", "forums", "templates"):
        with open(base / f"{name}.json", encoding="utf-8") as fh:
            pack[name] = json.load(fh)
    return pack


def currency(country: str) -> dict:
    """The pack-declared currency (code, symbol, locale). Defaults to KES."""
    meta = load_pack(country)["products"].get("_meta", {})
    return meta.get("currency", {"code": "KES", "symbol": "KES", "locale": "en-KE"})


def get_product(country: str, product_id: str) -> dict | None:
    for p in load_pack(country)["products"]["products"]:
        if p["id"] == product_id:
            return p
    return None


def get_lender(country: str, lender_id: str) -> dict | None:
    for ld in load_pack(country)["lenders"]["lenders"]:
        if ld["id"] == lender_id:
            return ld
    return None


def get_forum(country: str, forum_key: str) -> dict | None:
    for f in load_pack(country)["forums"]["forums"]:
        if f["key"] == forum_key:
            return f
    return None


def get_scenario(country: str, scenario_key: str) -> dict | None:
    for s in load_pack(country)["rules"]["scenarios"]:
        if s["key"] == scenario_key:
            return s
    return None


def provenance(citation: str | None, citation_date: str | None,
               enforcing_body: str | None = None,
               register_name: str | None = None) -> dict:
    """One consistent 'where this came from' object attached to every civic claim.

    The brief's trust constraint is "traceable to credible sources, show when it was
    last updated". Deni already stores a citation + date on every scenario, forum and
    lender; this shapes them into a single, uniform block so the UI renders provenance
    the SAME way under every statement, instead of each surface inventing its own. It
    adds no new claim: it only re-exposes fields already in the data pack.
    """
    return {
        "source": citation,
        "verified": citation_date,
        "enforcing_body": enforcing_body,
        "register": register_name,
        "kind": "source",
    }


def accountability_chain(country: str, scenario_key: str) -> dict | None:
    """The full civic chain for one right: right -> law -> every body with power over
    it -> the exact filing channel -> the document produced -> the citation.

    This is deni's Transparency-track core drawn as a map: it makes visible which
    public institutions are accountable for a given right and how a citizen reaches
    each one. It reads entirely from the data pack (scenario + its primary and 'also'
    forums); no step is AI-generated.
    """
    scenario = get_scenario(country, scenario_key)
    if not scenario:
        return None
    forum_keys: list[tuple[str, bool]] = []
    if scenario.get("forum_key"):
        forum_keys.append((scenario["forum_key"], True))
    for fk in scenario.get("also", []):
        forum_keys.append((fk, False))
    bodies = []
    for fk, primary in forum_keys:
        f = get_forum(country, fk)
        if not f:
            continue
        bodies.append({
            "key": fk,
            "name": f.get("name"),
            "primary": primary,
            "handles": f.get("handles"),
            "channel": f.get("channel"),
            "what_to_include": f.get("what_to_include", []),
            "document": f.get("template_id"),
            "provenance": provenance(f.get("source"), None, f.get("name")),
        })
    return {
        "key": scenario_key,
        "right": scenario.get("title"),
        "law_statement": scenario.get("law_statement"),
        "condition": scenario.get("condition"),
        "bodies": bodies,
        "body_count": len(bodies),
        "provenance": provenance(scenario.get("citation"),
                                 scenario.get("citation_date"),
                                 bodies[0]["name"] if bodies else None),
    }


def localize(entry: dict, field: str, lang: str) -> str | None:
    """Return a data-pack field in the requested language, falling back to English.

    Translations are HUMAN-AUTHORED and stored in the pack under an `i18n` block, e.g.
        {"title": "...", "i18n": {"sw": {"title": "..."}, "sheng": {"title": "..."}}}
    exactly like the fixed UI-string dictionary in the frontend. The AI model is NOT
    used to translate legal text: the law stays fixed, sourced data (R6/R14). A missing
    translation falls back to the English field, so a partially-translated pack (or an
    English-only pack like ZA) still renders.
    """
    if lang and lang != "en":
        translated = (entry.get("i18n", {}) or {}).get(lang, {}) or {}
        val = translated.get(field)
        if val:
            return val
    return entry.get(field)


def list_rights(country: str = "ke", lang: str = "en") -> dict:
    """Browsable know-your-rights view (Deni: access to information).

    Joins each scenario to its forum so a citizen can READ what the law says and
    where to go, before they ever have a problem. Pure read over the data pack;
    every entry carries its source and date (R7 trust/verification). Translatable
    fields resolve via `localize` (human-authored, English fallback); the citation,
    date and source are language-independent facts and are never translated.
    """
    pack = load_pack(country)
    forums = {f["key"]: f for f in pack["forums"]["forums"]}
    rights = []
    for s in pack["rules"]["scenarios"]:
        forum = forums.get(s.get("forum_key", ""), {})
        forum_name = localize(forum, "name", lang) if forum else None
        rights.append({
            "key": s["key"],
            "title": localize(s, "title", lang),
            "law_statement": localize(s, "law_statement", lang),
            "condition": localize(s, "condition", lang),
            "citation": s.get("citation"),
            "citation_date": s.get("citation_date"),
            "provenance": provenance(s.get("citation"), s.get("citation_date"),
                                     forum_name),
            "forum": {
                "name": forum_name,
                "handles": localize(forum, "handles", lang) if forum else None,
                "channel": localize(forum, "channel", lang) if forum else None,
            },
        })
    meta = pack["rules"].get("_meta", {})
    disclaimer = localize(meta, "disclaimer", lang) or (
        "This information is not legal advice. Recourse depends on the specific facts.")
    return {
        "rights": rights,
        "last_updated": meta.get("last_updated"),
        "disclaimer": disclaimer,
    }


def licence_authority(country: str) -> dict:
    """The pack-declared licensing authority config (makes licence checks country-agnostic).

    Falls back to the Kenya CBK/DCP defaults if a pack doesn't declare one.
    """
    meta = load_pack(country)["lenders"].get("_meta", {})
    la = meta.get("licence_authority")
    if la:
        return la
    return {
        "field": "cbk_dcp_licensed", "authority_short": "CBK",
        "authority_name": "the Central Bank of Kenya (CBK)",
        "register_name": "CBK licensed Digital Credit Providers register",
        "registered_label": "Licensed by CBK", "unregistered_label": "NOT on CBK licensed list",
        "registered_note": "is on CBK's licensed register.",
        "unregistered_note": "is not on CBK's licensed register.",
        "not_applicable_note": "is licensed under a different regime.",
    }


def check_lender(country: str, name: str) -> dict:
    """Look up a lender by (partial) name and return its licence/registration status.

    Checks a public fact against the pack-declared licensing authority (CBK in Kenya,
    NCR in South Africa, etc). Facts only, never an unsourced accusation.
    """
    la = licence_authority(country)
    field = la["field"]
    meta = load_pack(country)["lenders"].get("_meta", {})
    register_updated = meta.get("last_updated")
    if not (name or "").strip():
        return {"status": "unknown", "label": "Enter a lender name",
                "register_updated": register_updated,
                "note": f"Type a lender's name to check the {la['register_name']}."}
    name_l = name.strip().lower()
    for ld in load_pack(country)["lenders"]["lenders"]:
        if name_l in ld["name"].lower():
            lic = ld.get(field)
            # New schema: official_findings (regulator/court) vs reported_concerns
            # (press/context). Fall back to a legacy flat `findings` list if present.
            official = ld.get("official_findings")
            reported = ld.get("reported_concerns")
            if official is None and reported is None:
                official = ld.get("findings", [])
                reported = []
            base = {
                "matched": ld["name"], "authority": la["authority_short"],
                "register_name": la["register_name"], "register_updated": register_updated,
                "official_findings": official or [], "reported_concerns": reported or [],
                # Back-compat: keep a combined `findings` for any caller not yet updated.
                "findings": (official or []) + (reported or []),
                "regime": ld.get("regime"),
                # Register provenance: the licence status is a public fact; say where it
                # came from and when it was verified, in the same shape as every claim.
                "provenance": provenance(la.get("register_url"), register_updated,
                                         la.get("authority_name"), la.get("register_name")),
            }
            if lic is True:
                return {**base, "status": "licensed", "label": la["registered_label"],
                        "note": f"{ld['name']} {la['registered_note']}"}
            if lic is False:
                return {**base, "status": "unlicensed", "label": la["unregistered_label"],
                        "note": f"{ld['name']} {la['unregistered_note']}"}
            # not-applicable: lead with the regime it IS regulated under, not "not on list".
            regime = ld.get("regime") or la["not_applicable_note"]
            return {**base, "status": "not-applicable",
                    "label": f"Regulated under a different regime",
                    "note": f"{ld['name']}: {regime}"}
    return {"status": "unknown", "label": "Not in Deni's list",
            "official_findings": [], "reported_concerns": [], "findings": [],
            "register_name": la["register_name"], "register_updated": register_updated,
            "note": f"This lender isn't in Deni's dataset. Check the {la['register_name']} "
                    f"directly to confirm."}
