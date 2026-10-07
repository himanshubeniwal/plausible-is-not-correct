# Plausible Is Not Correct: Reliable LLM Use in Scientific Research

Hands-on workshop for bioinformatics and cheminformatics researchers · 22nd Herbstseminar of the Leipzig Bioinformatics
and Computational EvoDevo groups (Doubice, CZ, October 2026) · **Himanshu Beniwal**, ScaDS.AI / TU Dresden

> **The LLM proposes. A curated database decides.**
> Every demo turns an LLM answer into checkable claims and checks them against Crossref, PubMed, NCBI Gene, UniProt,
> PubChem, Wikidata and openFDA. No deep computer-science background is required.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/himanshubeniwal/plausible-is-not-correct/blob/main/notebooks/workshop_demos.ipynb)

## Materials

| | |
|---|---|
| **Slides** | [slides/plausible-is-not-correct.pdf](slides/plausible-is-not-correct.pdf) |
| **Workshop notes** | [01_workshop_notes.md](01_workshop_notes.md): the full content, with all demo results |
| **Cheat sheet** | [02_cheat_sheet.md](02_cheat_sheet.md): seven rules, prompt templates, database APIs |
| **AI research guidelines** | [03_ai_research_guidelines.md](03_ai_research_guidelines.md): prompting, tool choice, data protection, authorship, DFG/EU rules |
| **Tools** | [04_tools.md](04_tools.md): curated AI and database tools for bio- and cheminformatics |
| **References** | [references.md](references.md): every cited paper and policy, with DOI or link |
| **Notebook** | [notebooks/workshop_demos.ipynb](notebooks/workshop_demos.ipynb): six hands-on demos |

## Run the notebook

**Option A: Google Colab (nothing to install).** Click the badge above, then *Runtime → Run all*.

**Option B: on your computer** (Python 3.9 or newer):
```bash
git clone https://github.com/himanshubeniwal/plausible-is-not-correct.git
```
```bash
cd plausible-is-not-correct
```
```bash
pip install -r requirements.txt
```
```bash
jupyter lab notebooks/workshop_demos.ipynb
```
Optional extras: `pip install -r requirements-optional.txt` adds RDKit (local SMILES parsing) and the Anthropic SDK
(live Claude calls; Python 3.10 or newer).

### The six demos

| # | Demo | Ground truth |
|---|---|---|
| 1 | Are these references real? | Crossref, PubMed |
| 2 | Gene and protein facts | NCBI Gene, UniProtKB |
| 3 | Molecules and SMILES | PubChem, RDKit |
| 4 | Quote-grounded extraction from an abstract | the abstract |
| 5 | Knowledge graphs: supported, missing, or wrong | Wikidata, openFDA |
| 6 | Self-consistency and multilingual consistency | UniProtKB, NCBI Gene |

### LLM cells: three modes
| Mode | When | What happens |
|---|---|---|
| `manual` | default without an API key | the cell prints a prompt; paste it into any chatbot, paste the answer back, finish with a line `END` |
| `anthropic` | default when `ANTHROPIC_API_KEY` is set | calls Claude (`claude-opus-5-5`; change with `PLAUSIBLE_MODEL`) |
| `off` | set `PLAUSIBLE_LLM=off` | skips LLM cells; all prepared verification examples still run |

### Offline use
Database answers for all prepared examples ship in `data/cache/`. Set `PLAUSIBLE_OFFLINE=1` to use only the cache. Your own
live-LLM questions need internet for verification.

## Repository layout
```text
plausible/            verification helpers (literature, bio, chem, grounding, kg, llm)
notebooks/            workshop notebook, a pre-run copy, and the script that builds the notebook
data/cache/           cached database responses (offline mode)
slides/               slide deck (PDF), its HTML source (src/), and build_pdf.py
```

## Tested
From a fresh clone, the notebook runs end-to-end without errors on Python 3.9 (with RDKit) and Python 3.12 (with and without RDKit), online and offline, and on Python 3.12 with an empty cache, so every database query ran live. The live-LLM cells were tested with deliberately messy chatbot answers (extra prose, renamed keys, missing values, unknown genes, “1,480 aa”, Devanagari digits).

## Contact
Himanshu Beniwal · https://himanshubeniwal.github.io
