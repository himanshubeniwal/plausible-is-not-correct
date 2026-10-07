"""Knowledge-graph grounding with Wikidata (a free, public, SPARQL-queryable KG).

Key lesson: a knowledge graph is *incomplete*. If a triple is absent, that is
"not supported by this KG" — NOT "false". This is the open-world assumption.
"""
from __future__ import annotations

import networkx as nx

from .http import fetch

SPARQL = "https://query.wikidata.org/sparql"

# Wikidata properties used here (see https://www.wikidata.org/wiki/Property:P129 etc.)
P_INTERACTS = "P129"   # physically interacts with
P_TREATS = "P2175"     # medical condition treated


def sparql(query: str) -> list[dict]:
    data = fetch(SPARQL, params={"query": query, "format": "json"})
    rows = []
    for b in data["results"]["bindings"]:
        rows.append({k: v["value"] for k, v in b.items()})
    return rows


def drug_facts(drug_label: str) -> list[dict]:
    """Protein targets (P129) and treated conditions (P2175) for a drug, by English label."""
    q = f"""
    SELECT ?drug ?rel ?obj ?objLabel WHERE {{
      ?drug rdfs:label "{drug_label}"@en .
      VALUES ?rel {{ wdt:{P_INTERACTS} wdt:{P_TREATS} }}
      ?drug ?rel ?obj .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}"""
    rows = sparql(q)
    rel_name = {f"http://www.wikidata.org/prop/direct/{P_INTERACTS}": "interacts_with",
                f"http://www.wikidata.org/prop/direct/{P_TREATS}": "treats"}
    return [{"subject": drug_label, "relation": rel_name[r["rel"]],
             "object": r["objLabel"], "qid": r["obj"].rsplit("/", 1)[-1]} for r in rows]


def build_graph(triples: list[dict]) -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()
    for t in triples:
        g.add_edge(t["subject"].lower(), t["object"].lower(), relation=t["relation"], qid=t.get("qid"))
    return g


def check_triple(g: nx.MultiDiGraph, subject: str, relation: str, obj: str,
                 aliases: dict[str, list[str]] | None = None) -> str:
    """SUPPORTED if the KG contains the edge (allowing listed aliases for the object),
    otherwise NOT_IN_KG. We never return FALSE: absence is not evidence of falsity."""
    s = subject.lower()
    names = {obj.lower(), *[a.lower() for a in (aliases or {}).get(obj, [])]}
    if s not in g:
        return "NOT_IN_KG (subject unknown)"
    for _, o, d in g.out_edges(s, data=True):
        if d["relation"] == relation and any(n == o or n in o for n in names):
            return "SUPPORTED"
    return "NOT_IN_KG"


def fda_label_indications(generic_name: str) -> dict | None:
    """'Indications and usage' text of a current US drug label (openFDA), as a second source."""
    data = fetch("https://api.fda.gov/drug/label.json",
                 params={"search": f"openfda.generic_name:{generic_name}", "limit": 1})
    if not data or not data.get("results"):
        return None
    r = data["results"][0]
    return {"label_effective": r.get("effective_time"),
            "indications": " ".join(r.get("indications_and_usage", []))}


def mentioned_in(text: str, *phrases: str) -> bool:
    return any(p.lower() in text.lower() for p in phrases)
