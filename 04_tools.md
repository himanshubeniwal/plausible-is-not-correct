# Tools for AI-assisted research in bioinformatics and cheminformatics
*Plausible Is Not Correct · Herbstseminar 2026 · Himanshu Beniwal (ScaDS.AI / TU Dresden)*

A short, curated list. Every link and description was checked on 7 October 2026 against the project's own website or
GitHub repository. Licenses and terms change, so read them before use, especially for commercial work.

**Rule of thumb:** use AI models to *generate hypotheses and drafts*, and use curated databases to *verify*.

---

## 1. Literature and evidence

| Tool | What it does | Link |
|---|---|---|
| PubMed / NCBI E-utilities | biomedical literature search with a free API | https://pubmed.ncbi.nlm.nih.gov · https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ |
| Europe PMC | life-science literature search with a free REST API | https://europepmc.org |
| Semantic Scholar | literature search and citation graph with a free API | https://www.semanticscholar.org |
| Crossref | DOI metadata for checking references | https://api.crossref.org |
| PaperQA2 | open-source retrieval-augmented question answering over your PDFs, with citations | https://github.com/Future-House/paper-qa |
| Elicit | commercial AI assistant for paper search, data extraction and systematic reviews | https://elicit.com |
| Zotero | free, open-source reference manager | https://www.zotero.org |

## 2. Protein structure and design

| Tool | What it does | Link |
|---|---|---|
| AlphaFold Protein Structure Database | precomputed AlphaFold structure predictions | https://alphafold.ebi.ac.uk |
| AlphaFold Server | AlphaFold 3 web server for non-commercial use | https://alphafoldserver.com |
| AlphaFold 3 | inference code; model parameters subject to Google's terms of use (Abramson et al., 2024, *Nature*) | https://github.com/google-deepmind/alphafold3 |
| ColabFold | accessible structure prediction in Google Colab or locally (Mirdita et al., 2022, *Nat Methods*) | https://github.com/sokrypton/ColabFold |
| Boltz | open biomolecular interaction models (Boltz-1, Boltz-2: structure and binding affinity); code and weights under MIT | https://github.com/jwohlwend/boltz |
| Chai-1 | structure prediction for proteins, small molecules, DNA, RNA and glycosylations; needs Linux and a CUDA GPU | https://github.com/chaidiscovery/chai-lab |
| ESM | protein language models and structure prediction (ESMC, ESMFold2, ESM3); check each model's license | https://github.com/Biohub/esm |
| Foldseek | fast protein structure comparison and search; web server available | https://github.com/steineggerlab/foldseek · https://search.foldseek.com |
| ProteinMPNN | sequence design for given protein backbones (Dauparas et al., 2022, *Science*) | https://github.com/dauparas/ProteinMPNN |
| RFdiffusion | de novo protein backbone design (Watson et al., 2023, *Nature*) | https://github.com/RosettaCommons/RFdiffusion |

## 3. Genomics and single-cell

| Tool | What it does | Link |
|---|---|---|
| Biopython | Python toolkit for sequences, file formats and NCBI access | https://biopython.org |
| Evo 2 | DNA language model with up to 1 Mb context, for modeling and design | https://github.com/ArcInstitute/evo2 |
| Scanpy | single-cell analysis in Python | https://scanpy.scverse.org |
| scvi-tools | deep probabilistic models for single-cell and spatial omics | https://scvi-tools.org |
| scGPT | foundation model for single-cell multi-omics | https://github.com/bowang-lab/scGPT |

## 4. Chemistry and drug discovery

| Tool | What it does | Link |
|---|---|---|
| RDKit | open-source cheminformatics toolkit (parsing, descriptors, fingerprints) | https://www.rdkit.org/docs/ |
| PubChem | chemical structures and properties with the PUG-REST API | https://pubchem.ncbi.nlm.nih.gov |
| ChEMBL | curated bioactivity database with a REST API | https://www.ebi.ac.uk/chembl/ |
| DeepChem | deep-learning library for drug discovery, chemistry, materials and biology | https://deepchem.io |
| Chemprop | message-passing neural networks for molecular property prediction | https://github.com/chemprop/chemprop |
| DiffDock | diffusion-based molecular docking (DiffDock-L) | https://github.com/gcorso/DiffDock |
| REINVENT 4 | generative molecular design: de novo design, scaffold hopping, R-group replacement, linker design, optimisation | https://github.com/MolecularAI/REINVENT4 |
| Therapeutics Data Commons | datasets and benchmarks for therapeutic machine learning | https://tdcommons.ai |
| ChemCrow | LLM agent with chemistry tools; the public package omits some tools from the paper (M. Bran et al., 2024) | https://github.com/ur-whitelab/chemcrow-public |

## 5. AI agents and coding assistants

| Tool | What it does | Link |
|---|---|---|
| Biomni | general-purpose biomedical AI agent that plans and runs code; large software environment, needs LLM API keys | https://github.com/snap-stanford/Biomni |
| Jupyter AI | JupyterLab extension that connects AI agents to notebooks | https://github.com/jupyterlab/jupyter-ai |
| Claude Code | AI coding assistant for the terminal and IDEs | https://claude.com/claude-code |
| GitHub Copilot | AI coding assistant in editors and on GitHub | https://github.com/features/copilot |

Coding assistants speed up analysis code. Read and test what they write, and verify every package they import.

## 6. Running models locally (for sensitive data)

| Tool | What it does | Link |
|---|---|---|
| Ollama | run open-weight language models on your own machine | https://ollama.com |
| LM Studio | desktop app to download and run open-weight models locally | https://lmstudio.ai |
| Hugging Face Hub | repository of open models and datasets | https://huggingface.co |

## 7. Ground truth for verification

| Resource | Use it to check | Link |
|---|---|---|
| UniProtKB | protein names, sequences, lengths, functions | https://www.uniprot.org |
| NCBI Gene / Datasets | gene symbols, IDs, locations | https://www.ncbi.nlm.nih.gov/datasets/ |
| Ensembl | genomes, genes, transcripts, variants | https://www.ensembl.org |
| RCSB PDB | experimentally determined structures | https://www.rcsb.org |
| InterPro | protein families and domains | https://www.ebi.ac.uk/interpro/ |
| STRING | protein–protein association networks | https://string-db.org |
| Wikidata | general knowledge graph (SPARQL) | https://query.wikidata.org |
| openFDA | US drug labels | https://open.fda.gov |

## 8. Reproducible pipelines

| Tool | What it does | Link |
|---|---|---|
| Galaxy Europe | web-based, reproducible bioinformatics workflows | https://usegalaxy.eu |
| Bioconda | conda channel for bioinformatics software | https://bioconda.github.io |
| Google Colab | hosted Jupyter notebooks in the browser; runs this workshop's notebook | https://colab.research.google.com |
