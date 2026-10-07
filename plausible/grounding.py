"""Quote-grounding: "show me the sentence, or it didn't happen".

When an LLM extracts facts from a text, ask it to return the exact supporting
quote for each fact. Then check mechanically that each quote really occurs in
the source. This catches invented facts cheaply. It does NOT prove that the
quote actually supports the claim, so a human still reads the flagged and the
passed items. It just shrinks the search space.
"""
from __future__ import annotations

import json
import re
from difflib import SequenceMatcher


def _norm(s: str) -> str:
    s = s.replace(" ", " ").replace(" ", " ")
    s = re.sub(r"[‐-―]", "-", s)            # unify dashes
    s = re.sub(r"[‘’“”]", "'", s)  # unify quotes
    s = s.replace('"', "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def quote_in_source(quote: str, source: str, fuzzy_threshold: float = 0.9) -> tuple[str, float]:
    """EXACT if the quote appears verbatim (after whitespace/quote normalisation),
    FUZZY if a near-identical span exists (e.g. tiny paraphrase), else ABSENT."""
    q, src = _norm(quote), _norm(source)
    if not q:
        return "ABSENT", 0.0
    if q in src:
        return "EXACT", 1.0
    # slide a window of the quote's length over the source and keep the best ratio
    best, n = 0.0, len(q)
    step = max(1, n // 10)
    for i in range(0, max(1, len(src) - n + 1), step):
        r = SequenceMatcher(None, q, src[i:i + n]).ratio()
        best = max(best, r)
    return ("FUZZY" if best >= fuzzy_threshold else "ABSENT"), round(best, 2)


def parse_json_block(text: str):
    """Pull the first JSON array/object out of an LLM answer (handles ```json fences)."""
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    candidate = m.group(1) if m else text
    start = min([i for i in (candidate.find("["), candidate.find("{")) if i != -1], default=-1)
    if start == -1:
        raise ValueError("No JSON found in the model output")
    return json.JSONDecoder().raw_decode(candidate[start:])[0]


def check_extractions(items: list[dict], source: str, quote_key: str = "quote") -> list[dict]:
    out = []
    for it in items:
        status, score = quote_in_source(it.get(quote_key, ""), source)
        out.append({**it, "grounding": status, "match_score": score})
    return out
