# Plausible Is Not Correct — participant handout
*Herbstseminar 2026 · Himanshu Beniwal (ScaDS.AI / TU Dresden)*

> **The LLM proposes, a curated database decides.**
> Use LLMs where errors are cheap to detect, and design your workflow so that errors *become* cheap to detect.

## 1. Seven-point checklist
1. **Ask for identifiers, not names**: DOI, PMID, UniProt accession, NCBI Gene ID, HGNC symbol, PubChem CID, ChEBI/ChEMBL ID.
2. **Ask for structured output** (JSON / table), then **verify each field** programmatically.
3. **Extraction from documents → demand exact quotes**, check that they occur verbatim, and read the near-matches yourself.
4. **Allow abstention** ("use null if unsure"). Count abstentions separately from errors.
5. **Sample more than once.** Disagreement is a warning sign. Agreement is not proof.
6. **Knowledge graphs:** absent ≠ false, present ≠ true. Keep provenance (source, release, date) and triangulate high-stakes facts.
7. **Report LLM use like an instrument**: model + version, date, prompts, and what you verified against what.

## 2. Prompt patterns that make answers checkable

**Identifiers + abstention**
```
For each gene in [...], give the NCBI Gene ID and UniProt accession (reviewed, human).
Return ONLY JSON: [{"symbol":..., "ncbi_gene_id":..., "uniprot":...}]. Use null if you are not certain.
```
**Grounded extraction**
```
From the text below, extract every <entity/result>. Return JSON with keys: item, value, quote.
"quote" must be copied EXACTLY from the text. If the text does not state it, do not include the item.
TEXT: <<<paste>>>
```
**Neutral phrasing (avoid sycophancy)**
Use "Is X associated with Y? Give evidence for and against." Avoid "I think X causes Y. Explain why."

**Lookup, not recall (chemistry)**
Ask for *names or IDs* and get the structure from PubChem/ChEMBL. Do not ask the model to write SMILES from memory.

**Code**
Check every suggested package before installing it: does it exist on PyPI/Bioconductor/conda-forge, is it the intended
project, and is it maintained? LLMs invent package names (Spracklen et al., 2025).

## 3. Free, curated sources to verify against (all have REST APIs)

| What | Source | API entry point |
|---|---|---|
| DOIs / bibliographic metadata | Crossref | `https://api.crossref.org/works/{doi}` |
| Biomedical literature | PubMed (NCBI E-utilities) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` |
| Genes | NCBI Gene (same E-utilities, `db=gene`) | `esearch` / `esummary` |
| Proteins | UniProtKB | `https://rest.uniprot.org/uniprotkb/search` |
| Small molecules | PubChem PUG-REST | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/` |
| General life-science KG | Wikidata SPARQL | `https://query.wikidata.org/sparql` |
| US drug labels | openFDA | `https://api.fda.gov/drug/label.json` |

Be a good citizen: NCBI allows up to 3 requests/s without an API key. Cache your results.
Note that PubChem renamed its SMILES fields in 2025: `SMILES` is now the isomeric form and `ConnectivitySMILES` is the former canonical form.

## 4. Methods-section template
> "We used [model, version] via [interface/API] on [dates] to [task]. Prompts are provided in Supplement X.
> All [references / identifiers / extracted values] were verified against [database, release/date];
> [n] of [N] items were corrected or removed. The authors take full responsibility for the content."

Always check your journal's and institution's current AI policy.

## 5. Run the demos yourself
```
pip install -r requirements.txt          # rdkit and anthropic are optional
cd notebooks && jupyter lab workshop_demos.ipynb
```
- **No API key?** The notebook prints each prompt. Paste it into any chatbot and paste the answer back (end with a line `END`).
- **No internet?** `export PLAUSIBLE_OFFLINE=1` uses cached database answers.

## 6. Key reading (verified; full list in `references.md`)
- Huang et al. (2025) A survey on hallucination in LLMs. *ACM TOIS*. doi:10.1145/3703155
- Farquhar et al. (2024) Detecting hallucinations in LLMs using semantic entropy. *Nature*. doi:10.1038/s41586-024-07421-0
- Jin et al. (2024) GeneGPT. *Bioinformatics*. doi:10.1093/bioinformatics/btae075
- M. Bran et al. (2024) Augmenting LLMs with chemistry tools (ChemCrow). *Nat Mach Intell*. doi:10.1038/s42256-024-00832-8
- Pan et al. (2024) Unifying LLMs and knowledge graphs: a roadmap. *IEEE TKDE*. doi:10.1109/TKDE.2024.3352100
- Kumar, …, Beniwal, Hartvigsen & Sap (2025) PolyGuard. COLM 2025. arXiv:2504.04377
