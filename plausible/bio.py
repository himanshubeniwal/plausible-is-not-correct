"""Look up gene and protein facts in NCBI Gene and UniProtKB.

These are the "ground truth" sources we compare LLM claims against. They are
curated, versioned and citable — unlike an LLM's memory.
"""
from __future__ import annotations

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
    """Reviewed (Swiss-Prot) UniProt entry for a gene symbol in one organism."""
    query = f"gene_exact:{gene} AND organism_id:{taxon_id} AND reviewed:true"
    data = fetch(f"{UNIPROT}/search", params={
        "query": query, "format": "json", "size": 1,
        "fields": "accession,protein_name,gene_primary,length,mass,organism_name,cc_function,cc_subcellular_location",
    })
    results = (data or {}).get("results", [])
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


def compare(claimed, actual, kind: str = "exact", tol: float = 0.0) -> str:
    """Tiny comparison helper returning SUPPORTED / CONTRADICTED / NO_DATA."""
    if actual in (None, "", []):
        return "NO_DATA"
    if kind == "number":
        return "SUPPORTED" if abs(float(claimed) - float(actual)) <= tol else "CONTRADICTED"
    if kind == "contains":
        return "SUPPORTED" if str(claimed).lower() in str(actual).lower() else "CONTRADICTED"
    return "SUPPORTED" if str(claimed).strip().lower() == str(actual).strip().lower() else "CONTRADICTED"
