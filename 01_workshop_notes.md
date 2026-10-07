# Plausible Is Not Correct: Reliable LLM Use in Scientific Research
**Workshop notes · 22nd Herbstseminar, Doubice (CZ), October 2026 · Himanshu Beniwal, ScaDS.AI / TU Dresden**

> **The LLM proposes. A curated database decides.**

Companion material: [slides](slides/plausible-is-not-correct.pdf) · [notebook](notebooks/workshop_demos.ipynb) ·
[cheat sheet](02_cheat_sheet.md) · [AI research guidelines](03_ai_research_guidelines.md) ·
[tools](04_tools.md) · [references](references.md)

Every number below comes from the cited paper's abstract or from a live database query. The database results were recorded on 7 October 2026.

---

## Agenda (90 minutes)

| Time | Block |
|---|---|
| 0:00 | Warm-up: which of these seven references are real? |
| 0:05 | Part 1: Why plausible ≠ correct |
| 0:20 | Demos 1–2: references, gene and protein facts |
| 0:35 | Part 2: Mitigation toolbox and model reasoning |
| 0:45 | Demos 3–4: molecules, quote-grounded extraction |
| 0:58 | Part 3: Knowledge graphs and Demo 5 |
| 1:12 | Part 4: Inside the model, across languages, and Demo 6 |
| 1:24 | Take-home checklist and Q&A |

---

## Part 1: Why plausible ≠ correct

### What a large language model does
- It continues text with *likely* next tokens (word pieces), learned from its training data.
- By default it does not look anything up.
- Correct and incorrect answers come out equally fluent. **Fluency is not evidence.**

### Two kinds of error
(Huang et al., 2025, *ACM TOIS*; Ji et al., 2023, *ACM Computing Surveys*)

| Type | Meaning | Example |
|---|---|---|
| **Factuality** | conflicts with world knowledge | "BRCA1 is on chromosome 13" (it is on 17; BRCA2 is on 13) |
| **Faithfulness** | does not follow the given source or instruction | a summary that adds a number the abstract does not contain |

### Why it happens
1. **Long-tail knowledge.** Accuracy on a question tracks how many related documents the model saw during pre-training (Kandpal et al., 2023, ICML). Rare genes, species and compounds are exactly where research questions sit.
2. **Guessing is rewarded.** Training and benchmark scoring reward guessing over admitting uncertainty (Kalai et al., 2025).
3. **Sycophancy.** Assistants fine-tuned on human feedback tend to match the user's stated view (Sharma et al., 2024, ICLR). Keep your hypothesis out of the question.
4. **Snowballing.** Models defend their own early errors. Yet ChatGPT and GPT-4 recognised 67% and 87% of their own mistakes when asked separately (Zhang et al., 2024, ICML).

### Evidence

| Failure | Finding |
|---|---|
| Fabricated references | 55% of GPT-3.5 and 18% of GPT-4 citations fabricated (Walters & Wilder, 2023, *Sci Rep*) |
| …still in 2026 | ChatGPT-5: 7.13% of 2,736 references fabricated; 49.34% fully accurate (Bernstein et al., 2026, *Cureus*) |
| Atomic factual precision | ChatGPT: 58% of atomic facts in biographies supported (FActScore; Min et al., 2023, EMNLP) |
| Invented software packages | ≥5.2% (commercial) and 21.7% (open-source) hallucinated packages; 205,474 unique fake names (Spracklen et al., 2025, USENIX Security) |

**Working principle:** use LLMs where errors are cheap to detect, and design your workflow so that errors *become* cheap to detect.

---

## Demos 1–2: references, gene and protein facts

**Demo 1: seven constructed references, checked against Crossref and PubMed.**

| Reference | Verdict | Why |
|---|---|---|
| AlphaFold (Jumper 2021), correct DOI | VERIFIED | matches Crossref |
| BLAST (Altschul 1990), correct PMID | VERIFIED | matches PubMed |
| Gapped BLAST title + DOI of the 1990 BLAST paper | MISMATCH | the DOI belongs to another paper |
| AlphaFold with year 2020 | MISMATCH | the record says 2021 |
| Invented DOI `10.1038/s41586-023-99999-9` | NOT_FOUND | the DOI does not resolve |
| Clustal Omega, title only | FOUND_BY_TITLE | PMID 21988835 |
| Invented title, no identifier | UNVERIFIABLE | absent from PubMed, which does **not** prove it is fake |

A resolving DOI does not show that the paper supports your claim. That still requires reading the paper.

**Demo 2: gene and protein claims, checked against NCBI Gene and UniProtKB.**

| Claim | Database | Verdict |
|---|---|---|
| TP53 protein: 393 aa | UniProt P04637: 393 | supported |
| CFTR protein: 1480 aa | UniProt P13569: 1480 | supported |
| EGFR protein: 1210 aa | UniProt P00533: 1210 | supported |
| BRCA1 on chromosome 13 | NCBI Gene 672: 17q21.31 | **contradicted** |
| HBB on chromosome 11 | NCBI Gene 3043: 11p15.4 | supported |
| DMD on chromosome Y | NCBI Gene 1756: Xp21.2-p21.1 | **contradicted** |

Ask for **structured output (JSON)** and **identifiers**. Verification then becomes a loop over fields instead of a reading exercise.

**Verifiers need verifying too.** A UniProt search for the gene `HTT` returns two reviewed human entries: huntingtin
(P42858, official symbol HTT, 3,142 aa) and the serotonin transporter (P31645, official symbol SLC6A4, which lists HTT as a synonym, 630 aa).
A check that takes the first hit can wrongly mark a correct answer as false. Match on the **official symbol** or, better, on the accession.

---

## Part 2: Mitigation toolbox and model reasoning

| Lever | What it means | Example |
|---|---|---|
| Ask better | identifiers, JSON output, "null if unsure", neutral wording | Demo 2 prompt |
| Ground | give the source text and demand exact quotes (RAG: Lewis et al., 2020) | Demo 4; PaperQA (Lála et al., 2023) |
| Use tools | let the model query databases instead of recalling | GeneGPT: 0.83 average on GeneTuring vs 0.12 for ChatGPT (Jin et al., 2024, *Bioinformatics*); ChemCrow (M. Bran et al., 2024, *Nat Mach Intell*) |
| Measure uncertainty | sample several answers; disagreement signals confabulation | SelfCheckGPT (Manakul et al., 2023); semantic entropy (Farquhar et al., 2024, *Nature*) |
| Verify | check every claim against a curated source | this workshop's notebook |

**Lookup beats recall.** In GeneGPT, the same class of model went from 0.12 to 0.83 when it was allowed to query NCBI.

**Reasoning helps, but the written reasoning is not an explanation.**
- Step-by-step prompting (chain-of-thought) improves multi-step tasks (Wei et al., 2022). Majority voting over several reasoning paths helps further (self-consistency; Wang et al., 2023).
- Written reasoning can misstate *why* a model answered. When Turpin et al. (2023) biased inputs toward wrong answers, models wrote plausible rationalisations without mentioning the bias, and accuracy dropped by up to 36%.
- Treat reasoning as a draft argument to check.

**Avoid:**
- Asking "are you sure?" and accepting the reply. Models may flip or double down.
- Treating agreement between runs as proof.
- Pasting LLM-generated SMILES, identifiers or package names into a pipeline unchecked.

---

## Demos 3–4: molecules and quote grounding

**Demo 3: structures compared by InChIKey against PubChem.**

| Claim | Result |
|---|---|
| caffeine, paracetamol, ibuprofen | formula, weight and structure all correct |
| "aspirin" written as the methyl ester | **different molecule** |
| levodopa written with the wrong stereocentre (D-DOPA) | **same skeleton, different stereochemistry** |
| `C1=CC=CC=C1C(=O` | **invalid SMILES** |

Ask for a **name or identifier**, then look the structure up. Do not ask the model to write a structure from memory.
Note: PubChem renamed its SMILES fields in 2025. `SMILES` is now the isomeric form and `ConnectivitySMILES` the former canonical form. Code generated from older documentation can request fields that no longer exist.

**Demo 4: extraction from the GeneGPT abstract (PMID 38341654), with exact quotes required.**

| Extracted item | Quote check |
|---|---|
| GeneGPT 0.83 | EXACT |
| new Bing 0.44 | EXACT |
| ChatGPT 0.21 (abstract says 0.12) | FUZZY, score 0.94: a near-match hiding a changed number |
| GPT-4 0.71 (not in abstract) | ABSENT |

A quote check proves the text exists, not that it supports the claim. It shrinks what you must read, but it does not replace reading.

---

## Part 3: Knowledge graphs

A knowledge graph (KG) stores facts as `(subject, relation, object)` triples with identifiers, which makes claims checkable.
Life-science examples: Wikidata (Waagmeester et al., 2020, *eLife*), Hetionet (Himmelstein et al., 2017, *eLife*) and PrimeKG (Chandak et al., 2023, *Sci Data*).

Three ways to combine LLMs and KGs (Pan et al., 2024, *IEEE TKDE*):
1. **KG-enhanced LLMs:** retrieve triples to ground or check answers.
2. **LLM-augmented KGs:** extract candidate triples from text. Verify them before adding them to the graph.
3. **Synergised:** both directions, iteratively.

**Demo 5: imatinib in Wikidata vs the current US drug label (openFDA).**

| Claim | Wikidata | FDA label |
|---|---|---|
| interacts with ABL1 | supported | — |
| interacts with KIT | supported | — |
| interacts with EGFR | not in KG | — (EGFR is not an imatinib target) |
| treats chronic myeloid leukemia | **not in KG** | **listed** |
| treats acute myeloid leukemia | **in KG** | **not listed** |
| treats gastrointestinal stromal tumor | in KG | listed |

**Three lessons**
1. **Absent ≠ false.** KGs follow the open-world assumption, so "not in KG" mixes true and false claims.
2. **Present ≠ true.** Curated and crowd-sourced graphs contain errors.
3. **Context and provenance matter.** "Treats" depends on approval status, population, source and version. Record them, and triangulate high-stakes facts across independent sources.

Related work by the speaker: *From Universal Knowledge Graphs to Contextual Semantic Contracts* (Beniwal & Färber, ISWC 2026).

---

## Part 4: Inside the model and across languages

**Where facts live in a model**
- **Knowledge neurons:** specific neurons in BERT whose activation correlates with expressing a given fact. Editing them can update or erase that fact without fine-tuning (Dai et al., 2022, ACL).
- **ROME:** causal tracing localises factual recall to mid-layer feed-forward modules. A rank-one weight edit updates a single association (Meng et al., 2022, NeurIPS).
- **Cross-lingual editing (XME):** a fact is edited in one language and its propagation measured in others. Experiments used BLOOM, mBERT and XLM-RoBERTa on Latin-script (English, French, Spanish) and Indic-script (Hindi, Gujarati, Bengali) languages. Editing methods showed clear limitations, especially across script families (Beniwal, Nandagopan D & Singh, Findings of EACL 2024).
- **Where Does Toxicity Live?** The Meow2X and TRNE methods localise toxicity to specific layers and neurons using activation differences, then suppress it by inference-time scaling or rank-one weight edits, without gradient descent. Results span 5 LMs, 2 benchmarks and 90 configurations: toxicity is concentrated in early MLP layers, and single-evaluator setups underestimate it (Beniwal & Singh, 2026, preprint).

**Reliability and safety are not language-neutral**
- **PolyGuard:** a multilingual safety moderation model for 17 languages. It was trained on PolyGuardMix (1.91M samples) and evaluated on PolyGuardPrompts (29K samples), both built from real multilingual interactions plus human-verified translations of WildGuardMix. It outperforms existing open-weight and commercial safety classifiers by 5.5% (Kumar, …, Beniwal, Hartvigsen & Sap, COLM 2025).
- **Multilingual jailbreaks:** without any deliberate attack, low-resource languages had about 3× the likelihood of harmful output compared with high-resource languages (Deng et al., 2024, ICLR).
- **Cross-lingual sycophancy:** 6 models, 1.1M instances, 38 languages. Sycophancy rises sharply in low-resource and zero-shot languages, and tokenizer fertility is a structural driver (Shah, Beniwal, Singh & Silpasuwanchai, 2026, preprint).
- **Breaking mBad!** Cross-lingual detoxification across 392 settings reveals trade-offs between safety and knowledge preservation (Beniwal et al., MELT @ COLM 2025).

**Demo 6:** ask for the CFTR protein length five times and compare with UniProt (1480 aa). Then ask for the chromosome of HBB in English, German, Czech and Hindi and compare with NCBI Gene (chromosome 11).

---

## Take-home checklist
1. Ask for **identifiers**, not names.
2. Ask for **structured output**, then **verify every field** against a curated database.
3. Demand **exact quotes** when extracting. Check them mechanically and read the near-matches.
4. **Allow abstention.** Count it separately from errors.
5. **Sample more than once.** Disagreement is a warning; agreement is not proof.
6. **KG absence ≠ false; KG presence ≠ true.** Keep provenance and triangulate.
7. **Report AI use like an instrument:** model, version, date, prompts, and what was verified against what.

**Example methods statement (illustrative)**
> "We used Claude Opus 5.5 (Anthropic; API; 1–14 October 2026) to extract gene–disease associations from 120 PubMed abstracts. Prompts are provided in Supplementary File S2. Every extracted association was checked for an exact supporting quote and against NCBI Gene (accessed 15 October 2026); 9 of 412 items were corrected and 14 removed. The authors take full responsibility for the content."
