# Plausible Is Not Correct: Reliable LLM Use in Scientific Research
**Facilitator guide · 22nd Herbstseminar (Doubice, CZ, 4–9 Oct 2026) · Himanshu Beniwal, ScaDS.AI / TU Dresden**

Every factual claim below that cites a paper has been checked against the paper's record: Crossref, PubMed, or the
arXiv API (abstracts read on 2026-10-07). Numbers are quoted only where they appear in the abstract. Full list:
[`references.md`](references.md). Items marked **[YOU]** need your own words, because they concern unpublished or
not-yet-public details of your work.

---

## 0. Format at a glance

| | |
|---|---|
| **Audience** | Bioinformatics / cheminformatics students and researchers; *no deep CS background assumed* |
| **Default length** | 90 min (60- and 120-min variants at the end) |
| **Hands-on** | `notebooks/workshop_demos.ipynb` — runs **with or without** an API key, and **offline** from cache |
| **Core message** | *The LLM proposes, a curated database decides.* Make claims checkable, then check them. |
| **Venue note** | The venue is rural (Doubice, CZ), so don't count on good Wi-Fi. `PLAUSIBLE_OFFLINE=1` runs all database checks from the cache, and `workshop_demos_executed.ipynb` keeps pre-run outputs as a fallback. |

### Agenda (90 min)

| Time | Block | Mode |
|---|---|---|
| 0:00–0:05 | Hook: "Which of these 7 references are real?" | live poll |
| 0:05–0:20 | **Part 1 — Why plausible ≠ correct** | talk |
| 0:20–0:35 | Demo 1 (references) + Demo 2 (genes/proteins) | hands-on |
| 0:35–0:45 | **Part 2 — Mitigation toolbox & model reasoning** | talk |
| 0:45–0:58 | Demo 3 (SMILES) + Demo 4 (quote grounding) | hands-on |
| 0:58–1:12 | **Part 3 — Knowledge graphs** + Demo 5 | talk + hands-on |
| 1:12–1:24 | **Part 4 — Inside the model & across languages** + Demo 6 | talk + hands-on |
| 1:24–1:30 | Take-home checklist, reporting LLM use, Q&A | discussion |

---

## Hook (5 min)

**Slide H1. "Which of these references are real?"**
Show the 7 references from Demo 1 (notebook cell 3), without verdicts. Ask for a show of hands for each one.
Then run the cell.

*Speaker notes.* The references were constructed for teaching. One has a nonexistent DOI. One is a real title attached
to another paper's DOI. One has the wrong year. One is invented with no identifier. Most people cannot tell by
looking, and that is the point. Fluency is not evidence.

---

## Part 1 — Why plausible ≠ correct (15 min)

**Slide 1.1. What an LLM actually does (no CS needed)**
- An LLM is trained to continue text with *likely* next tokens (word pieces).
- It does not look facts up by default. It reproduces patterns in its training data.
- The result reads like expert text whether or not the content is right.

*Speaker notes.* An analogy for biologists: a model that has read millions of methods sections can write a convincing
one for an experiment that never happened. Fluency and correctness are produced by the same machinery, so fluency cannot be a signal of correctness.

**Slide 1.2. Two kinds of hallucination** (Huang et al., 2025, *ACM TOIS*; Ji et al., 2023, *ACM Comput. Surv.*)
- **Factuality errors.** The output conflicts with world knowledge. Example: "BRCA1 is on chromosome 13." It is on 17; BRCA2 is on 13.
- **Faithfulness errors.** The output does not follow the given source or instructions. Example: a summary of an abstract that adds a number not in the abstract.
- For research both matter. Faithfulness errors are especially dangerous in literature work and data extraction.

**Slide 1.3. Why it happens (four well-supported reasons)**
1. **Long-tail knowledge.** Accuracy on a fact depends on how often related documents appear in pre-training data
   (Kandpal et al., 2023, ICML). Rare genes, organisms, and compounds are exactly where research questions live.
2. **Guessing is rewarded.** Training and benchmark grading reward guessing over saying "I don't know"
   (Kalai et al., 2025, arXiv 2509.04664).
3. **Sycophancy.** Models fine-tuned on human feedback tend to agree with the user's stated view, and humans sometimes prefer
   convincing sycophantic answers over correct ones (Sharma et al., 2024, ICLR). Practical rule: don't put your hypothesis into the question.
4. **Snowballing.** A model that commits to an early error keeps justifying it. In Zhang et al. (2024, ICML), ChatGPT and
   GPT-4 could recognise 67% and 87% of their own mistakes when asked separately.

**Slide 1.4. The evidence, in our own field's currency**

| Failure | Evidence (from the abstracts) |
|---|---|
| Fabricated references | 55% of GPT-3.5 and 18% of GPT-4 citations fabricated (Walters & Wilder, 2023, *Sci Rep*) |
| …still in 2026 | ChatGPT-5: 7.13% of 2,736 references fabricated; only 49.34% fully accurate (Bernstein et al., 2026, *Cureus*) |
| Atomic factual precision | ChatGPT: 58% of atomic facts in biographies supported (FActScore; Min et al., 2023, EMNLP) |
| Invented software packages | Hallucinated packages in ≥5.2% (commercial) and 21.7% (open-source) of cases; 205,474 unique fake package names (Spracklen et al., 2025, USENIX Security) |

*Speaker notes.* The trend is improving, but it is not zero, and you cannot tell which 7% are wrong without checking.
The package result matters for bioinformaticians: `pip install` or `conda install` of an LLM-suggested package name is a
software supply-chain risk. Check that the package exists, is the one you mean, and is maintained.

**Slide 1.5. The working principle**
> Use LLMs where errors are **cheap to detect**, and design your workflow so that errors **become** cheap to detect.

→ Switch to the notebook: Demo 1 & 2.

---

## Demos 1 & 2 (15 min)

**Demo 1 — references.** Run the constructed list, then the live cell (the LLM proposes 5 references with DOIs).
Discussion points:
- `UNVERIFIABLE` ≠ fake. PubMed doesn't index everything (arXiv, conference papers).
- A resolving DOI does not mean the paper supports the claim. That still requires reading.

**Demo 2 — gene/protein facts.** Constructed claims, then the live JSON cell.
Discussion points:
- Ask for **structured output** (JSON). Then verification is a loop, not a reading exercise.
- "Canonical isoform" is a UniProt convention. Under-specified questions produce "errors" that are really ambiguity.
- Allowing `null` (abstention) is a feature. Count abstentions separately from errors.

---

## Part 2 — Mitigation toolbox & model reasoning (10 min)

**Slide 2.1. Five levers, from cheapest to most involved**

| Lever | What it is | Example in bio/chem |
|---|---|---|
| **Ask better** | Ask for identifiers, structured output, explicit "null if unsure", no leading hypotheses | Demo 2 prompt |
| **Ground** | Put the source text in the prompt and demand exact quotes (retrieval-augmented generation, RAG; Lewis et al., 2020, NeurIPS) | Demo 4; PaperQA (Lála et al., 2023) |
| **Use tools** | Let the model call databases instead of recalling facts | GeneGPT: NCBI Web APIs, avg. 0.83 on GeneTuring vs 0.12 for ChatGPT (Jin et al., 2024, *Bioinformatics*); ChemCrow (M. Bran et al., 2024, *Nat Mach Intell*) |
| **Measure uncertainty** | Sample several answers; disagreement signals confabulation | SelfCheckGPT (Manakul et al., 2023); semantic entropy (Farquhar et al., 2024, *Nature*) |
| **Verify** | Check each claim against a curated source | This whole notebook |

*Speaker notes.* The GeneGPT numbers make a useful contrast. The same class of model goes from 0.12 to 0.83 on the same
benchmark when it is allowed to query NCBI instead of answering from memory. The lesson is not "use GeneGPT". The lesson is that **lookup beats recall**.

**Slide 2.2. Reasoning: helpful, but don't read it as an explanation**
- Asking for step-by-step reasoning (chain-of-thought) improves performance on many multi-step tasks (Wei et al., 2022, NeurIPS).
  Sampling several reasoning paths and taking the majority answer helps further (self-consistency; Wang et al., 2023, ICLR).
- **But** the written reasoning can misrepresent *why* the model answered. When Turpin et al. (2023, NeurIPS) biased inputs toward wrong answers, models
  wrote plausible rationalisations without mentioning the bias, and accuracy dropped by up to 36% on BIG-Bench Hard tasks.
- So: treat the reasoning as **a draft argument to check**, not as a log of what the model computed.

**Slide 2.3. What *not* to do**
- Don't ask the same model "are you sure?" and accept the answer. It may flip (sycophancy) or double down (snowballing).
- Don't treat agreement between runs as proof. Models can be consistently wrong. Demo 6 shows this.
- Don't paste LLM-generated SMILES, gene IDs, or package names into a pipeline unchecked.

→ Demo 3 & 4.

---

## Demos 3 & 4 (13 min)

**Demo 3 — molecules.** Comparing by **InChIKey** catches a methyl ester posing as aspirin, the wrong levodopa
enantiomer (D-DOPA: same skeleton, different stereo block), and an unparsable SMILES.
Key point: ask the LLM for the **name or identifier**, then look the structure up. Don't ask it to write SMILES.
Side note to share: PubChem renamed its SMILES fields in 2025. `SMILES` is now the isomeric form and
`ConnectivitySMILES` is the old canonical form. Code generated by an LLM trained on older docs will request a field that no longer exists. That is a small, real instance of outdated knowledge.

**Demo 4 — quote grounding.** Uses the GeneGPT abstract (PMID 38341654) fetched live.
- EXACT → the text exists. FUZZY 0.94 → *almost* the text: the altered number (ChatGPT 0.21 instead of 0.12). ABSENT → invented.
- Quote matching proves that the text exists, not that it supports the claim. It shrinks what a human must read. It does not replace reading.

---

## Part 3 — Knowledge graphs (14 min incl. Demo 5)

**Slide 3.1. What a KG is**
Facts as `(subject, relation, object)` triples with identifiers. Example: `imatinib —physically interacts with→ ABL1`.
Life-science examples: Wikidata (Waagmeester et al., 2020, *eLife*), Hetionet (Himmelstein et al., 2017, *eLife*),
PrimeKG (Chandak, Huang & Zitnik, 2023, *Sci Data*).

**Slide 3.2. Three ways to combine LLMs and KGs** (Pan et al., 2024, *IEEE TKDE*)
1. **KG-enhanced LLMs.** Retrieve triples to ground or check answers (Demo 5).
2. **LLM-augmented KGs.** Use LLMs to extract candidate triples from text. These must be verified before they enter the KG.
3. **Synergised.** Both directions, iteratively.

**Demo 5 (live).** Query Wikidata for imatinib, check claims, then triangulate with the FDA label (openFDA).
Results when this guide was prepared (2026-10-07):
- `imatinib → ABL1`, `→ KIT`: **supported**.
- `imatinib → EGFR`: **not in KG**. Correctly so; EGFR is not an imatinib target.
- `imatinib treats CML`: **not in KG**, yet Ph+ CML is the first indication on the FDA label.
- `imatinib treats AML`: **in KG**, yet AML does not appear on the FDA label.

**Slide 3.3. Three lessons**
1. **Absent ≠ false.** KGs follow the open-world assumption. "Not in KG" mixes true and false claims.
2. **Present ≠ true.** Curated and crowd-sourced KGs contain errors.
3. **Context and provenance matter.** "Treats" depends on context: approved, off-label, investigational, in which population, according to which source and which version.

**Slide 3.4. Your research: contextual meaning in KGs** **[YOU]**
*"From Universal Knowledge Graphs to Contextual Semantic Contracts"* (Beniwal & Färber, ISWC 2026, accepted).
The PDF is not public yet, so I have not summarised its content. Add 2–3 sentences in your own words. The imatinib/AML example above
is a natural bridge: the same triple can be "true" under one context (some study, some source) and "false" under another (the regulatory label).

---

## Part 4 — Inside the model & across languages (12 min incl. Demo 6)

**Slide 4.1. Where do facts "live" in a model?**
- **Knowledge neurons.** Specific neurons in BERT whose activation correlates with expressing a given fact. Editing them can
  update or erase that fact without fine-tuning (Dai et al., 2022, ACL).
- **ROME.** Causal tracing points to mid-layer feed-forward (MLP) modules. A rank-one weight edit can update one factual association
  (Meng et al., 2022, NeurIPS).
- Why researchers should care: if facts are localised, they can (in principle) be **corrected without retraining**. Every edit must then be checked for side effects.

**Slide 4.2. Your work on editing and localisation**
- **Cross-lingual editing (XME)** (Beniwal, Nandagopan D & Singh, EACL Findings 2024). A fact is edited in one language and the
  propagation is measured in others, using BLOOM, mBERT, and XLM-RoBERTa across Latin-script (English, French, Spanish) and Indic-script (Hindi,
  Gujarati, Bengali) languages. State-of-the-art editing methods showed clear limitations, especially across **different script families**.
  → *A correction made in English may not reach the Hindi (or Czech?) version of the "same" knowledge.*
- **Where Does Toxicity Live?** (Beniwal & Singh, 2026, arXiv 2605.27997, preprint). Meow2X and TRNE localise toxicity to
  specific **layers and neurons** from activation differences between toxic and neutral prompts. They then suppress it via inference-time
  scaling or minimal **rank-one weight edits**, without gradient descent. Evaluated on 5 LMs, 2 benchmarks, and 90 configurations.
  Toxicity is disproportionately encoded in **early MLP layers**, and single-evaluator setups underestimate it, which argues for
  multi-evaluator assessment.
  → *Methodological lesson for everyone: one judge (human or model) is not enough.*

**Slide 4.3. Safety and reliability are not language-neutral**
- **PolyGuard** (Kumar, Jain, Yerukola, Jiang, Beniwal, Hartvigsen & Sap, COLM 2025). A multilingual safety moderation model for
  **17 languages**. It is trained on PolyGuardMix (**1.91M** samples) and evaluated on PolyGuardPrompts (**29K** samples). Both combine real
  multilingual human–LLM interactions with human-verified translations of WildGuardMix. Labels cover prompt harmfulness, response
  harmfulness, and response refusal. The authors report it outperforms existing open-weight and commercial safety classifiers by 5.5%.
- **Multilingual jailbreaks** (Deng et al., 2024, ICLR). In unintentional settings, low-resource languages had about **3×** the likelihood
  of harmful content compared with high-resource languages, for both ChatGPT and GPT-4.
- **Cross-lingual sycophancy** (Shah, Beniwal, Singh & Silpasuwanchai, 2026, arXiv 2606.08451, preprint). 6 instruction-tuned models,
  **1.1M** instances, **38 languages**, 33 topics. Sycophancy rises sharply in low-resource and zero-shot languages, and tokenizer
  fertility is identified as a structural driver.
- **Breaking mBad!** (Beniwal, Kim, Sap, Dan & Hartvigsen, MELT @ COLM 2025). Cross-lingual detoxification across 392 settings
  reveals trade-offs between safety and knowledge preservation.

*Speaker notes.* The bridge to this audience: many of you write, read, or query in German, Czech, or another language,
and many bio resources are English-only. Reliability measured in English does not automatically carry over.

**Demo 6 (live LLM only).** (a) Ask for the CFTR length 5× and compare with UniProt (1480 aa). (b) Ask for the HBB
chromosome in English, German, Czech, and Hindi and compare with NCBI Gene (chr 11). *Ask native speakers in the room to check the translations.*
If there is no API key, do it with the room: everyone asks their own chatbot, and you tally the answers on the board.

---

## Close (6 min)

**Slide C1. Take-home checklist** (also in the handout)
1. Ask for **identifiers**, not names.
2. Ask for **structured output**, then **verify each field** against a curated database.
3. Demand **exact quotes** when extracting. Check them mechanically, then read the FUZZY ones.
4. **Allow abstention**.
5. **Sample more than once**. Disagreement is a warning, agreement is not proof.
6. **KG absence ≠ false; KG presence ≠ true**. Keep provenance and triangulate.
7. **Report LLM use** like an instrument: model + version, date, prompts, and what was verified, how.

**Slide C2. Reporting template for your methods section**
> "We used [model, version] via [interface/API] on [dates] to [task]. Prompts are provided in Supplement X. All
> [references / identifiers / extracted values] were verified against [database, release/date]; [n] of [N] items were
> corrected or removed. The authors take full responsibility for the content."

Also check your target journal's and your university's current AI policy. These change frequently.

---

## Variants

- **60 min.** Hook → Part 1 (10) → Demos 1+2 (12) → Part 2, short (6) → Demo 4 (8) → Part 3 + Demo 5 (12) → Close (5). Mention Part 4 in one slide.
- **120 min.** Add 15 min of free exploration (participants verify LLM answers about *their own* gene, protein, or compound of interest), and give Part 4 an extra 10 min.

## Pre-flight checklist (the night before)
- [ ] `pip install -r requirements.txt` on the presentation laptop; open the notebook; *Run All* with `PLAUSIBLE_LLM=off` → no errors.
- [ ] Run once with `PLAUSIBLE_OFFLINE=1` → no errors (proves the cache is complete).
- [ ] If using the API: set `ANTHROPIC_API_KEY`; run the live cells once (they also fill the cache for those prompts).
- [ ] Re-run Demo 5 online if possible. Wikidata may have been edited since 2026-10-07, so adapt your narration to what it shows.
- [ ] Fill in slide 3.4 **[YOU]**.
- [ ] Export slides to PDF for the seminar's user page / USB stick (the organisers ask for a PDF).
