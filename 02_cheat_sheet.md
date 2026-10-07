# Cheat sheet: reliable LLM use in research
*Plausible Is Not Correct · Herbstseminar 2026 · Himanshu Beniwal (ScaDS.AI / TU Dresden)*

> **The LLM proposes. A curated database decides.**

## Seven rules
1. **Identifiers, not names:** DOI, PMID, UniProt accession, NCBI Gene ID, HGNC symbol, PubChem CID, ChEMBL ID.
2. **Structured output** (JSON or table), then **verify every field** programmatically.
3. **Exact quotes** for anything extracted from a document. Check them mechanically and read the near-matches.
4. **Allow abstention** ("use null if not certain").
5. **Sample more than once.** Disagreement is a warning; agreement is not proof.
6. **Knowledge graphs:** absent ≠ false, present ≠ true. Record source, release and date.
7. **Report AI use:** model, version, dates, prompts, and what was verified against what.

## Prompt templates

**Identifiers with abstention**
```text
For each human gene in this list: TP53, CFTR, HBB
give the NCBI Gene ID and the reviewed UniProt accession.
Return ONLY JSON: [{"symbol": "...", "ncbi_gene_id": "...", "uniprot": "..."}].
Use null for any value you are not certain about.
```

**Quote-grounded extraction**
```text
From the text below, extract every reported result.
Return ONLY JSON with keys: item, value, quote.
"quote" must be copied exactly from the text. Omit anything the text does not state.
TEXT:
<paste the text here>
```

**Neutral wording:** ask "Is X associated with Y? List evidence for and against, with PMIDs." Avoid "Explain why X causes Y."

**Chemistry:** ask for names or PubChem CIDs, then retrieve structures from PubChem or ChEMBL.

**Code:** before installing a suggested package, confirm on PyPI, Bioconductor or conda-forge that it exists, is the intended project, and is maintained.

## Free databases with REST APIs

| Purpose | Source | Endpoint |
|---|---|---|
| DOI metadata | Crossref | `https://api.crossref.org/works/{doi}` |
| Literature | PubMed (NCBI E-utilities) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` |
| Literature | Europe PMC | `https://www.ebi.ac.uk/europepmc/webservices/rest/search` |
| Genes | NCBI Gene (E-utilities, `db=gene`) | `esearch.fcgi`, `esummary.fcgi` |
| Proteins | UniProtKB | `https://rest.uniprot.org/uniprotkb/search` |
| Small molecules | PubChem PUG-REST | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/` |
| Bioactivity | ChEMBL | `https://www.ebi.ac.uk/chembl/api/data/` |
| Knowledge graph | Wikidata SPARQL | `https://query.wikidata.org/sparql` |
| US drug labels | openFDA | `https://api.fda.gov/drug/label.json` |

NCBI allows up to 3 requests per second without an API key. Cache your results.

## Safety in one minute
- Do not paste patient data, unpublished results, confidential manuscripts or grant proposals into consumer chatbots. Use local models or institution-approved services.
- Genetic and health data are special categories of personal data under GDPR Art. 9(1).
- AI tools cannot be authors. You remain responsible for every sentence, number and reference.
- Disclose substantial AI use in the methods section.

Full guidance: [03_ai_research_guidelines.md](03_ai_research_guidelines.md) · Tools: [04_tools.md](04_tools.md)
