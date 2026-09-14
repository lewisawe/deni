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
