# Using AI in research: prompts, tools, and safety
*Plausible Is Not Correct · Herbstseminar 2026 · Himanshu Beniwal (ScaDS.AI / TU Dresden)*

A practical guide for bioinformatics and cheminformatics researchers. Policy statements are taken from the primary
documents listed at the end, checked on 7 October 2026. Policies change, so check the current versions before you rely on them.

---

## 1. Where AI helps, and where it needs a safety net

| Task | Good fit? | Safety net |
|---|---|---|
| Explaining a method, concept or error message | yes | cross-check with documentation |
| Writing or refactoring analysis code | yes | read the code, run tests, check every imported package |
| Drafting text from **your own** notes and results | yes | you check every claim; disclose substantial use |
| Literature discovery | yes, as a starting point | resolve every DOI/PMID and read the papers you cite |
| Extracting values from papers | with care | demand exact quotes, verify against the source |
| Facts about genes, proteins and molecules | only with lookup | verify against NCBI, UniProt, PubChem, ChEMBL |
| Generating structures (SMILES) or identifiers from memory | avoid | retrieve from databases instead |
| Peer review, proposal evaluation | restricted | follow funder and journal rules (Section 5) |

---

## 2. Prompting for checkable answers

**A good research prompt contains five parts:** task · context or source text · output format · rules for uncertainty · what to leave out.

```text
Task:     Extract all reported binding affinities from the abstract below.
Context:  <paste abstract>
Format:   Return ONLY JSON: [{"compound": "...", "target": "...", "value": "...", "unit": "...", "quote": "..."}]
Rules:    "quote" must be copied exactly from the abstract. Use null if a field is not stated.
Exclude:  Do not add values from other sources or from memory.
```

**Patterns that reduce errors**
- **Ask for identifiers** (DOI, PMID, UniProt, PubChem CID). Identifiers can be checked; prose cannot.
- **Provide the source.** Paste the abstract, table or documentation instead of relying on the model's memory.
- **Ask for JSON** so you can verify each field in code.
- **Allow "I don't know"** explicitly ("use null if not certain").
- **Use neutral wording.** "What is the evidence for and against X?" instead of "Why is X true?" Assistants tend to agree with the view stated in the prompt (Sharma et al., 2024).
- **Split the work:** one step generates, a separate step verifies against a database.
- **Ask again.** Re-run important questions. Inconsistent answers flag likely errors.
- **Keep a log:** model name and version, date, prompt and output. The same input can produce different outputs.

**Patterns to avoid**
- "Are you sure?" as verification. Models may flip or defend an error (Zhang et al., 2024).
- Reading the model's step-by-step reasoning as an explanation of how it decided (Turpin et al., 2023).
- Long chats that mix tasks. Start a new conversation for each task.

---

## 3. Choosing tools

1. **Prefer tools that look things up** (databases, retrieval over your PDFs) over tools that answer from memory.
2. **Prefer outputs with identifiers and links.**
3. **Prefer open, documented tools** whose model, version and license you can name in your methods section.
4. **Check the license and terms.** Example: AlphaFold Server is for non-commercial use, and AlphaFold 3 model parameters are subject to Google's terms of use.
5. **Check compute needs.** Example: Chai-1 requires Linux, Python 3.10 or later and a CUDA GPU.

A curated, verified list: [04_tools.md](04_tools.md).

---

## 4. Data protection and confidentiality

- **Treat everything you type into a cloud chatbot as leaving your institution.** Providers may store inputs or use them for training, depending on the product and settings.
- **Personal data:** genetic data and data concerning health are special categories under **GDPR Art. 9(1)**. Do not enter patient-level or participant-level data into external AI services unless your data-protection officer has approved that service.
- **Unpublished work:** the EU guidelines ask researchers not to upload their own or others' unpublished work to external AI systems without assurance that the data will not be reused, for example for training.
- **Safer options:** run open models locally (e.g. Ollama, LM Studio) or use services operated by your university under a data-processing agreement. Turn off chat history and training options where available.
- **Never paste credentials:** API keys, passwords, tokens, server addresses.

---

## 5. Integrity, authorship, disclosure, review

| Rule | Source |
|---|---|
| AI tools are not authors; humans are accountable for all content | ICMJE; EU living guidelines (2026); DFG statement (2023) |
| Disclose AI use: which tools, for what purpose, to what extent | DFG statement (2023); EU living guidelines (2026); ICMJE |
| Disclose substantial use in the methods section; tool name, version and date; share prompts and outputs where relevant | EU living guidelines (2026) |
| Never use AI to fabricate, falsify or manipulate research data | EU living guidelines (2026), citing the ALLEA Code of Conduct |
| AI-generated content cannot be cited as a primary source | ICMJE |
| Failure to disclose may require correction and can be treated as misconduct | ICMJE |
| **EU:** refrain from substantial AI use in sensitive activities such as peer review and proposal evaluation | EU living guidelines (2026) |
| **DFG reviewers (since 16 April 2026):** AI may be used only in a supporting role (e.g. finding literature, turning your own notes into prose, language edits). Proposal content may be entered only into systems that run locally, are hosted by a trustworthy institution, or are contractually barred from storing or training on inputs, with those settings switched on. Content-relevant use must be disclosed when submitting the review. | DFG Vordruck 4.04 (03/26) |

Journals add their own rules. Read your target journal's AI policy before submission.

---

## 6. Code, software and reproducibility

- **Package names can be invented.** Commercial models hallucinated packages in at least 5.2% of cases and open-source models in 21.7% (Spracklen et al., 2025). Confirm a package exists and is the intended project before installing it.
- **Run generated code in an isolated environment** (virtual environment or container) and read it before you run it.
- **Test on known answers** before trusting code on new data.
- **Pin versions** of software, databases and models; record database release dates.

---

## 7. Biosafety and dual use

- Use AI within your institution's biosafety, ethics and export-control rules, as you would any other method.
- Do not use AI to plan the creation or enhancement of harmful biological agents or toxins.
- Some AI providers run safety filters that decline certain biology requests. These can also block benign work. Do not try to circumvent them; use databases and established tools instead.

---

## 8. One-page checklist
- No personal, confidential or unpublished data sent to an unapproved service
- Every reference resolved (DOI/PMID) and read
- Every gene, protein, compound and number checked against a curated database
- Every extracted value backed by an exact quote
- Generated code read, tested and run in an isolated environment; packages verified
- Model, version, dates and prompts recorded
- AI use disclosed according to journal and funder rules

---

## Primary sources
- European Commission, ERA Forum (2026). *Living guidelines on the responsible use of generative AI in research*, third version, May 2026. https://research-and-innovation.ec.europa.eu/document/2b6cf7e5-36ac-41cb-aab5-0d32050143dc_en
- DFG (2023). *Statement by the Executive Committee on the influence of generative models of text and image creation on science and the humanities and on the DFG's funding activities.* https://www.dfg.de/download/pdf/dfg_im_profil/geschaeftsstelle/publikationen/stellungnahmen_papiere/2023/230921_statement_executive_committee_ki_ai.pdf
- DFG (2026). *Leitlinie zur Nutzung von Künstlicher Intelligenz in der Begutachtung*, Vordruck 4.04 (03/26). https://www.dfg.de/resource/blob/387664/4-04-de.pdf · overview: https://www.dfg.de/AI
- ICMJE. *Recommendations: AI use by authors.* https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html
- Regulation (EU) 2016/679 (GDPR), Article 9. https://gdpr-info.eu/art-9-gdpr/
- Research papers cited here are listed in [references.md](references.md).
