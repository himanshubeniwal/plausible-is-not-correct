"""Small HTTP helper with an on-disk cache so the demos also run offline.

Every response we fetch is saved under data/cache/. Set the environment
variable PLAUSIBLE_OFFLINE=1 to *only* use cached responses (useful when the
venue Wi-Fi is weak). Cached answers are real API responses, recorded with the
date they were fetched.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import requests

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "PlausibleIsNotCorrect-Workshop/1.0 (educational; python-requests)"

TIMEOUT = 60   # seconds per request
RETRIES = 4    # attempts per request, with exponential back-off

# NCBI allows 3 requests/second without an API key; we stay below that.
_MIN_INTERVAL = {"eutils.ncbi.nlm.nih.gov": 0.4}
_last_call: dict[str, float] = {}


def offline() -> bool:
    return os.environ.get("PLAUSIBLE_OFFLINE", "0") == "1"


def _key(method: str, url: str, params: dict | None, data: dict | None) -> str:
    raw = json.dumps([method, url, params or {}, data or {}], sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


def _throttle(url: str) -> None:
    host = url.split("/")[2]
    wait = _MIN_INTERVAL.get(host, 0.0)
    elapsed = time.time() - _last_call.get(host, 0.0)
    if elapsed < wait:
        time.sleep(wait - elapsed)
    _last_call[host] = time.time()


def fetch(url: str, params: dict | None = None, data: dict | None = None,
          as_json: bool = True, headers: dict | None = None) -> Any:
    """GET (or POST when `data` is given) with cache-first behaviour.

    Returns parsed JSON (default) or text. Returns None for HTTP 404 (not found)
    and 400 (e.g. PubChem: unparsable SMILES), so callers can treat these as a
    verdict rather than a crash. Both are cached too.
    """
    method = "POST" if data is not None else "GET"
    key = _key(method, url, params, data)
    path = CACHE_DIR / f"{key}.json"

    if path.exists():
        cached = json.loads(path.read_text())
        return cached["body"]
    if offline():
        raise RuntimeError("PLAUSIBLE_OFFLINE=1 is set, but this request is not in the cache "
                           f"(only the prepared examples are cached): {url} {params or ''}")

    h = {"User-Agent": USER_AGENT}
    h.update(headers or {})
    resp, last_error = None, None
    for attempt in range(RETRIES):
        _throttle(url)
        try:
            resp = requests.request(method, url, params=params, data=data, headers=h, timeout=TIMEOUT)
        except (requests.ConnectionError, requests.Timeout) as e:
            last_error, resp = e, None
        else:
            if resp.status_code not in (429, 500, 502, 503, 504):
                break
            last_error = f"HTTP {resp.status_code}"
        if attempt < RETRIES - 1:
            time.sleep(2 ** attempt)      # 1 s, 2 s, 4 s
    if resp is None or resp.status_code in (429, 500, 502, 503, 504):
        host = url.split("/")[2]
        raise RuntimeError(
            f"{host} did not respond after {RETRIES} attempts ({last_error}). "
            "Check your internet connection, or set os.environ['PLAUSIBLE_OFFLINE'] = '1' "
            "to use the cached answers for the prepared examples.")
    if resp.status_code in (400, 404):
        body = None
    else:
        resp.raise_for_status()
        body = resp.json() if as_json else resp.text
    path.write_text(json.dumps({
        "fetched": time.strftime("%Y-%m-%d"),
        "method": method, "url": url, "params": params, "data": data,
        "status": resp.status_code, "body": body,
    }))
    return body
