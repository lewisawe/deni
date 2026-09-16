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


def list_rights(country: str = "ke") -> dict:
    """Browsable know-your-rights view (Deni: access to information).

    Joins each scenario to its forum so a citizen can READ what the law says and
    where to go, before they ever have a problem. Pure read over the data pack;
    every entry carries its source and date (R7 trust/verification).
    """
    pack = load_pack(country)
    forums = {f["key"]: f for f in pack["forums"]["forums"]}
    rights = []
    for s in pack["rules"]["scenarios"]:
        forum = forums.get(s.get("forum_key", ""), {})
        rights.append({
            "key": s["key"],
            "title": s["title"],
            "law_statement": s["law_statement"],
            "condition": s.get("condition"),
            "citation": s.get("citation"),
            "citation_date": s.get("citation_date"),
            "forum": {
                "name": forum.get("name"),
                "handles": forum.get("handles"),
                "channel": forum.get("channel"),
            },
        })
    return {
        "rights": rights,
        "last_updated": pack["rules"].get("_meta", {}).get("last_updated"),
        "disclaimer": pack["rules"].get("_meta", {}).get(
            "disclaimer",
            "This information is not legal advice. Recourse depends on the specific facts.",
        ),
    }


def check_lender(country: str, name: str) -> dict:
    """Look up a lender by (partial) name and return its CBK licence status.

    Checks a public fact: is this lender on CBK's licensed Digital Credit Providers
    register? Facts only — never an unsourced accusation.
    """
    name_l = (name or "").strip().lower()
    if not name_l:
        return {"status": "unknown", "label": "Enter a lender name",
                "note": "Type a lender's name to check the CBK register."}
    for ld in load_pack(country)["lenders"]["lenders"]:
        if name_l in ld["name"].lower():
            lic = ld.get("cbk_dcp_licensed")
            if lic is True:
                return {"status": "licensed", "label": "Licensed by CBK",
                        "matched": ld["name"],
                        "note": f"{ld['name']} is on CBK's licensed Digital Credit "
                                f"Providers list (verify current status at cbk.go.ke)."}
            if lic is False:
                return {"status": "unlicensed", "label": "NOT on CBK licensed list",
                        "matched": ld["name"],
                        "note": f"{ld['name']} is not on CBK's licensed DCP list. Under a "
                                f"2026 court ruling, an unlicensed digital lender may not "
                                f"be able to lawfully enforce repayment."}
            return {"status": "not-applicable", "label": "Not a CBK digital lender",
                    "matched": ld["name"],
                    "note": f"{ld['name']}: {ld.get('regime', 'licensed under a different regime')}"}
    return {"status": "unknown", "label": "Not in Deni's list",
            "note": "This lender isn't in Deni's dataset. Check CBK's licensed DCP "
                    "register directly at cbk.go.ke to confirm."}
