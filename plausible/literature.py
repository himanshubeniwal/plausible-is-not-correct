"""Check literature references against Crossref and PubMed (NCBI E-utilities).

A reference an LLM gives you can fail in three different ways:
  1. the identifier (DOI / PMID) does not exist at all,
  2. the identifier exists but points to a *different* paper,
  3. the paper exists but the claimed authors/year/journal are wrong.
`check_reference` tests all three.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher

from .http import fetch

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _norm(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")          # drop HTML/MathML tags
    text = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def title_similarity(a: str, b: str) -> float:
    """0..1 similarity of two titles after normalisation."""
    return round(SequenceMatcher(None, _norm(a), _norm(b)).ratio(), 2)


# ---------------------------------------------------------------- Crossref
def crossref_lookup(doi: str) -> dict | None:
    """Metadata for a DOI from Crossref, or None if the DOI is not registered there."""
    doi = doi.strip().removeprefix("https://doi.org/").removeprefix("doi:")
    data = fetch(f"https://api.crossref.org/works/{doi}")
    if not data:
        return None
    m = data["message"]
    year = None
    for field in ("published-print", "published-online", "issued"):
        parts = m.get(field, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    return {
        "doi": m.get("DOI"),
        "title": (m.get("title") or [""])[0],
        "journal": (m.get("container-title") or [""])[0],
        "year": year,
        "first_author": (m.get("author") or [{}])[0].get("family"),
    }


# ---------------------------------------------------------------- PubMed
def pubmed_summary(pmid: str) -> dict | None:
    """Title/journal/year/DOI for a PubMed ID, or None if it does not exist."""
    data = fetch(f"{EUTILS}/esummary.fcgi", params={"db": "pubmed", "id": str(pmid), "retmode": "json"})
    rec = (data or {}).get("result", {}).get(str(pmid))
    if not rec or "error" in rec:
        return None
    doi = next((a["value"] for a in rec.get("articleids", []) if a["idtype"] == "doi"), None)
    return {
        "pmid": str(pmid),
        "title": rec.get("title", "").rstrip("."),
        "journal": rec.get("source"),
        "year": int(rec["pubdate"][:4]) if rec.get("pubdate", "")[:4].isdigit() else None,
        "first_author": (rec.get("authors") or [{}])[0].get("name"),
        "doi": doi,
    }


def pubmed_search(query: str, retmax: int = 5) -> list[str]:
    """PMIDs matching a PubMed query string (e.g. a title in quotes with [ti])."""
    data = fetch(f"{EUTILS}/esearch.fcgi",
                 params={"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax})
    return data["esearchresult"]["idlist"]


def pubmed_abstract(pmid: str) -> dict:
    """Title + abstract text of a PubMed record (parsed from EFetch XML)."""
    xml = fetch(f"{EUTILS}/efetch.fcgi",
                params={"db": "pubmed", "id": str(pmid), "retmode": "xml"}, as_json=False)
    root = ET.fromstring(xml)
    title = "".join(root.find(".//ArticleTitle").itertext())
    parts = []
    for node in root.findall(".//Abstract/AbstractText"):
        label = node.get("Label")
        text = "".join(node.itertext()).strip()
        parts.append(f"{label}: {text}" if label else text)
    return {"pmid": str(pmid), "title": title, "abstract": "\n".join(parts)}


# ---------------------------------------------------------------- verdicts
def check_reference(ref: dict, min_title_sim: float = 0.85) -> dict:
    """Verify one reference dict with keys: title, and optionally doi, pmid, year, first_author.

    Returns the reference plus a verdict:
      VERIFIED       identifier exists and title (and year, if given) match
      MISMATCH       identifier exists but points to something else / wrong metadata
      NOT_FOUND      identifier does not resolve
      FOUND_BY_TITLE no identifier given, but PubMed has a matching title
      UNVERIFIABLE   no identifier and no title match (does NOT prove it is fake)
    """
    out = dict(ref)
    notes = []
    record = None

    if ref.get("doi"):
        record = crossref_lookup(ref["doi"])
        source = "Crossref"
    elif ref.get("pmid"):
        record = pubmed_summary(ref["pmid"])
        source = "PubMed"
    else:
        title = ref.get("title") or ""
        # all longer title words as [ti] terms; punctuation breaks exact-phrase search
        words = [w for w in re.sub(r"[^A-Za-z0-9 ]", " ", title).split() if len(w) > 3]
        if not words:
            out.update(verdict="UNVERIFIABLE", matched=None, notes="no identifier and no usable title")
            return out
        hits = pubmed_search(" AND ".join(f"{w}[ti]" for w in words), retmax=5)
        for pmid in hits:
            cand = pubmed_summary(pmid)
            if cand and title_similarity(cand["title"], title) >= min_title_sim:
                out.update(verdict="FOUND_BY_TITLE", matched=cand, notes=f"PMID {pmid}")
                return out
        out.update(verdict="UNVERIFIABLE", matched=None,
                   notes="no identifier; no title match in PubMed (check Google Scholar / bioRxiv)")
        return out

    if record is None:
        out.update(verdict="NOT_FOUND", matched=None, notes=f"identifier does not resolve in {source}")
        return out

    sim = title_similarity(record["title"], ref.get("title", ""))
    if sim < min_title_sim:
        notes.append(f"title similarity {sim} — identifier belongs to: '{record['title'][:80]}'")
    if ref.get("year") and record.get("year") and int(ref["year"]) != int(record["year"]):
        notes.append(f"year claimed {ref['year']} vs record {record['year']}")
    if ref.get("first_author") and record.get("first_author"):
        if _norm(ref["first_author"]).split()[0] not in _norm(record["first_author"]):
            notes.append(f"first author claimed {ref['first_author']} vs record {record['first_author']}")

    out.update(verdict="MISMATCH" if notes else "VERIFIED", matched=record,
               notes="; ".join(notes) or f"matches {source} record")
    return out
