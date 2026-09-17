"""Source-integrity check for Deni's civic data (run before recording a demo).

Every civic claim in Deni is traceable to a URL. If a citation is dead or moved, the
"traceable to credible sources" promise breaks in front of a judge. This walks every
country pack, collects every URL (lender findings, forum sources, rule citations,
authority register URLs), and checks each one is reachable.

Usage:
    python -m backend.check_sources            # all packs
    python -m backend.check_sources ke         # one country

Exit code is non-zero if any link is dead, so it can gate a release. Network failures
(no internet) are reported as "unchecked", not "dead", so an offline run is honest
rather than a false alarm.
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path

from .data_pack import DATA_DIR, load_pack

_URL_KEYS = ("citation", "source", "register_url", "verify_url", "cbk_licensed_source")


def _collect_urls(country: str) -> list[tuple[str, str]]:
    """Return (where, url) pairs for every URL-bearing field in a pack."""
    pack = load_pack(country)
    found: list[tuple[str, str]] = []

    def scan(obj, where: str) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in _URL_KEYS and isinstance(v, str) and v.startswith("http"):
                    found.append((where + "." + k, v))
                else:
                    scan(v, where + "." + str(k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                scan(v, f"{where}[{i}]")

    for name in ("lenders", "forums", "rules"):
        scan(pack[name], f"{country}/{name}")
    return found


def _check(url: str, timeout: float = 8.0) -> tuple[str, str]:
    """Return (status, detail). status is 'ok' | 'dead' | 'unchecked'."""
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "Deni-source-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.status
        return ("ok", str(code)) if code < 400 else ("dead", str(code))
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD (405) or bots (403) but the page is fine; retry GET.
        if e.code in (403, 405, 400):
            try:
                req.method = "GET"
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return ("ok", str(resp.status)) if resp.status < 400 else ("dead", str(resp.status))
            except Exception as e2:  # noqa: BLE001
                return ("dead", f"{e.code}->{type(e2).__name__}")
        return ("dead", str(e.code))
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        # No network / DNS / timeout: we cannot conclude the link is dead.
        return ("unchecked", type(e).__name__)


def main(argv: list[str]) -> int:
    countries = [c for c in argv[1:] if not c.startswith("-")]
    if not countries:
        countries = sorted(p.name for p in DATA_DIR.iterdir() if p.is_dir())

    dead: list[tuple[str, str, str]] = []
    unchecked = 0
    total = 0
    for cc in countries:
        print(f"\n== {cc} ==")
        for where, url in _collect_urls(cc):
            total += 1
            status, detail = _check(url)
            mark = {"ok": "OK  ", "dead": "DEAD", "unchecked": "??  "}[status]
            print(f"  [{mark}] {where}\n         {url}  ({detail})")
            if status == "dead":
                dead.append((where, url, detail))
            elif status == "unchecked":
                unchecked += 1

    print(f"\nChecked {total} URLs: {len(dead)} dead, {unchecked} unchecked (network).")
    if dead:
        print("DEAD LINKS (fix before demo):")
        for where, url, detail in dead:
            print(f"  - {where}: {url} ({detail})")
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv))
