"""plausible: small, transparent verification helpers for the workshop
"Plausible Is Not Correct: Reliable LLM Use in Scientific Research".

Every function queries a public, curated resource (Crossref, PubMed, NCBI Gene,
UniProt, PubChem, Wikidata) so that LLM output can be checked, not trusted.
"""
from . import bio, chem, grounding, kg, literature, llm  # noqa: F401
