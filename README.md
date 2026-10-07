# Plausible Is Not Correct: Reliable LLM Use in Scientific Research
Hands-on workshop · 22nd Herbstseminar of the Leipzig Bioinformatics & Computational EvoDevo groups (Doubice, 4–9 Oct 2026)
Himanshu Beniwal · ScaDS.AI / TU Dresden

**One idea runs through the whole workshop: the LLM proposes, a curated database decides.** Every demo turns an LLM answer
into checkable claims and checks them against Crossref, PubMed, NCBI Gene, UniProt, PubChem, Wikidata, or openFDA.

## What's here

| File | For whom | What |
|---|---|---|
| [`01_facilitator_guide.md`](01_facilitator_guide.md) | presenter | 90-min agenda, slide-by-slide content, speaker notes, 60/120-min variants, pre-flight checklist |
| [`02_participant_handout.md`](02_participant_handout.md) | participants | checklist, prompt patterns, API table, methods-section template |
| [`references.md`](references.md) | everyone | every cited paper, with DOI/arXiv ID, checked on 2026-10-07 |
| [`notebooks/workshop_demos.ipynb`](notebooks/workshop_demos.ipynb) | everyone | the 6 hands-on demos |
| [`notebooks/workshop_demos_executed.ipynb`](notebooks/workshop_demos_executed.ipynb) | presenter | same notebook with pre-run outputs (LLM cells skipped) as a fallback |
| [`notebooks/build_notebook.py`](notebooks/build_notebook.py) | maintainer | regenerates the notebook from source |
| [`plausible/`](plausible/) | everyone | small, readable verification helpers used by the notebook |
| `data/cache/` | — | cached real API responses, so database checks run offline |

## Setup
```bash
pip install -r requirements.txt
```
```bash
cd notebooks && jupyter lab workshop_demos.ipynb
```
`rdkit` (local SMILES parsing) and `anthropic` (live Claude calls) are optional. Without RDKit, structures are checked through PubChem.

## LLM backends (`PLAUSIBLE_LLM`)
- `anthropic`: the default when `ANTHROPIC_API_KEY` is set. Model: `PLAUSIBLE_MODEL` (default `claude-opus-5-5`; set
  `claude-haiku-5-5` for a cheaper run). Requests on Opus/Sonnet enable server-side refusal fallback. Occasionally a biology
  question can trip a safety classifier, and the notebook then prints `[MODEL DECLINED THIS REQUEST]`.
- `manual`: the default without a key. Each prompt is printed; paste it into **any** chatbot and paste the answer back,
  ending with a line `END`. This lets participants use whatever assistant they already have.
- `off`: skip LLM calls. All verification demos with constructed examples still run.

## Offline
```bash
export PLAUSIBLE_OFFLINE=1
```
Database answers then come only from `data/cache/`. The whole notebook runs offline with `PLAUSIBLE_LLM=off`. Live-LLM
cells produce new questions that are not in the cache, so their verification needs internet.

## What was tested (2026-10-07)
- The notebook executes end-to-end with **0 errors**, online and with `PLAUSIBLE_OFFLINE=1` (LLM backend `off`).
- The chemistry checks give identical verdicts with RDKit 2025.09 and via the PubChem fallback.
- The Anthropic call path was exercised up to authentication (SDK 1.12 accepted the request; a valid key was not available
  here). **Run the live cells once with your key before the session.**
- Live Wikidata content can change. Demo 5's narration reflects the state on 2026-10-07 (imatinib: AML listed, CML not
  listed). The openFDA cell re-checks the label live.
