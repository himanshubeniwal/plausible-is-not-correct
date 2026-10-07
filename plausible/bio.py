"""Look up gene and protein facts in NCBI Gene and UniProtKB.

These are the "ground truth" sources we compare LLM claims against. They are
curated, versioned and citable — unlike an LLM's memory.
"""
from __future__ import annotations

import re

from .http import fetch

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
UNIPROT = "https://rest.uniprot.org/uniprotkb"


def ncbi_gene(symbol: str, organism: str = "Homo sapiens") -> dict | None:
    """Official NCBI Gene record for an exact gene symbol in one organism."""
    term = f'{symbol}[sym] AND "{organism}"[orgn]'
    ids = fetch(f"{EUTILS}/esearch.fcgi",
                params={"db": "gene", "term": term, "retmode": "json"})["esearchresult"]["idlist"]
    if not ids:
        return None
    for gid in ids:  # pick the record whose official symbol matches exactly
        rec = fetch(f"{EUTILS}/esummary.fcgi",
                    params={"db": "gene", "id": gid, "retmode": "json"})["result"][gid]
        if rec.get("name", "").upper() == symbol.upper():
            return {
                "gene_id": gid,
                "symbol": rec["name"],
                "full_name": rec.get("description"),
                "chromosome": rec.get("chromosome"),
                "map_location": rec.get("maplocation"),
                "aliases": rec.get("otheraliases"),
                "organism": rec["organism"]["scientificname"],
                "summary": rec.get("summary"),
            }
    return None


def uniprot_protein(gene: str, taxon_id: int = 9606) -> dict | None:
    """Reviewed (Swiss-Prot) UniProt entry whose *primary* gene name is `gene`.

    UniProt's gene_exact search also matches synonyms: "HTT" is the official symbol
    of huntingtin but also an alias of SLC6A4 (serotonin transporter). We therefore
    keep only the entry whose primary gene name equals the query.
    """
    query = f"gene_exact:{gene} AND organism_id:{taxon_id} AND reviewed:true"
    data = fetch(f"{UNIPROT}/search", params={
        "query": query, "format": "json", "size": 25,
        "fields": "accession,protein_name,gene_primary,length,mass,organism_name,cc_function,cc_subcellular_location",
    })
    results = [r for r in (data or {}).get("results", [])
               if r.get("genes") and r["genes"][0].get("geneName", {}).get("value", "").upper() == gene.upper()]
    if not results:
        return None
    e = results[0]
    function = next((c["texts"][0]["value"] for c in e.get("comments", [])
                     if c.get("commentType") == "FUNCTION" and c.get("texts")), None)
    locations = []
    for c in e.get("comments", []):
        if c.get("commentType") == "SUBCELLULAR LOCATION":
            for loc in c.get("subcellularLocations", []):
                locations.append(loc["location"]["value"])
    return {
        "accession": e["primaryAccession"],
        "protein_name": e["proteinDescription"]["recommendedName"]["fullName"]["value"],
        "gene": e["genes"][0]["geneName"]["value"],
        "length_aa": e["sequence"]["length"],
        "mass_da": e["sequence"]["molWeight"],
        "organism": e["organism"]["scientificName"],
        "function": function,
        "subcellular_location": sorted(set(locations)),
    }


def first_number(text) -> int | None:
    """First integer in a free-text answer: '1,480 aa' -> 1480, 'Chromosom 11' -> 11.
    Also reads non-Latin digits (e.g. Devanagari '११' -> 11)."""
    t = re.sub(r"(?<=\d)[,.\u202f\u00a0 ](?=\d{3}\b)", "", str(text))   # drop thousands separators
    m = re.search(r"\d+", t)
    return int(m.group()) if m else None


def norm_chromosome(text) -> str | None:
    """Chromosome named in a free-text answer: 'chr17', '17q21.31', 'Chromosom 11',
    'गुणसूत्र ११' -> '17' / '11'; 'X', 'Xp21.2', 'on the Y chromosome' -> 'X' / 'Y'."""
    t = str(text)
    num = re.search(r"\d+", t)
    sex = re.search(r"(?<![A-Za-z])(?:chr)?([XxYy])(?![a-oq-zA-OQ-Z])", t)
    if num and (not sex or num.start() < sex.start()):
        return str(int(num.group()))
    return sex.group(1).upper() if sex else None


def compare(claimed, actual, kind: str = "exact", tol: float = 0.0) -> str:
    """Compare an LLM claim with a database value: SUPPORTED / CONTRADICTED / UNPARSABLE / NO_DATA.
    kind: "exact" (case-insensitive text), "number", "chromosome", or "contains"."""
    if actual in (None, "", []):
        return "NO_DATA"
    if kind == "number":
        c = first_number(claimed)
        if c is None:
            return "UNPARSABLE"
        return "SUPPORTED" if abs(c - float(actual)) <= tol else "CONTRADICTED"
    if kind == "chromosome":
        c = norm_chromosome(claimed)
        if c is None:
            return "UNPARSABLE"
        return "SUPPORTED" if c == norm_chromosome(actual) else "CONTRADICTED"
    if kind == "contains":
        return "SUPPORTED" if str(claimed).lower() in str(actual).lower() else "CONTRADICTED"
    return "SUPPORTED" if str(claimed).strip().lower() == str(actual).strip().lower() else "CONTRADICTED"
