# Research Ideation and Innovation: Literature Review and Skill Design

**English** | [简体中文](literature-review.zh-CN.md)

Verified on **2026-10-22**. This review covers literature-grounded scientific ideation, analogical transfer, candidate evolution, and the evaluation of idea quality and execution utility.

The papers were selected for methodological relevance; this is not an exhaustive systematic review. Technical claims draw on papers, official proceedings, author code, and original abstracts. Review depth distinguishes selected full-text sections from abstract-only access. Inaccessible full texts are not represented as having been read in depth. Machine-readable records are available in [bibliography.json](bibliography.json).

## Contents

1. Method families
2. Thirteen core works
3. Key tradeoffs
4. Synthesis into this skill
5. Scope and limitations

## 1. Method families

| Method family | Representative works | Corresponding skill operations |
|---|---|---|
| Literature evidence and limitations of close prior work | P01, P02, P03, P04 | Evidence ledger, near-miss methods, concrete failure mechanisms |
| Cross-domain structural transfer and facet recombination | P01, P05, P07, P13 | Shared structure, adaptation steps, failure boundaries |
| Research trajectories and candidate evolution | P06, P08 | Development chains, anonymous comparisons, bounded revision |
| Experimental execution and reliability | P09, P11, P12 | Minimal discriminating experiments, budgets, stopping rules |
| Limits of human and model evaluation | P01, P10, P11 | Independent review, separate feasibility assessment, explicit uncertainty |

## 2. Thirteen core works

### P01 · IdeaScientist: Orchestrating Agents for Grounded Scientific Ideation

- **Authors and version:** Jiarui Liu et al.; arXiv preprint, v2 (2026-10-09).
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2610.04074v2).
- **Review depth:** Selected full-text sections (`full_text_sections`).
- **Core contribution:** Stage-specific artifacts and references reconstructed from human papers support training individual roles. The main results evaluate research proposals without executing the proposed experiments.
- **Skill adaptation:** Use stage-specific evidence and mechanism transfer as workflow principles; do not claim to reproduce its GRPO training.

### P02 · SciMON: Scientific Inspiration Machines Optimized for Novelty

- **Authors and version:** Qingyun Wang, Doug Downey, Heng Ji, Tom Hope; ACL 2024.
- **Primary source:** [Paper / official page](https://aclanthology.org/2024.acl-long.18/).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Retrieve prior papers as inspirations, then repeatedly compare candidate ideas with prior work and revise them.
- **Skill adaptation:** Make novelty retrieval a recurring check rather than a one-off self-assessment.

### P03 · ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models

- **Authors and version:** Jinheon Baek et al.; NAACL 2025.
- **Primary source:** [Paper / official page](https://aclanthology.org/2025.naacl-long.342/).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Starting from a seed paper, expand knowledge through paper relationships and shared entities, then use reviewer feedback to refine questions, methods, and experiments.
- **Skill adaptation:** Identify nearby literature and concepts before separating generation from review.

### P04 · SciPIP: An LLM-based Scientific Paper Idea Proposer

- **Authors and version:** Wenxiao Wang et al.; arXiv preprint, v2 (2025-02-17).
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2410.23166v2).
- **Review depth:** Selected full-text sections (`full_text_sections`).
- **Core contribution:** Combine semantic, keyword, and co-occurrence retrieval, and integrate literature-driven generation with generation based on the model's internal knowledge.
- **Skill adaptation:** Broaden coverage through multiple retrieval and generation routes, then complete the supporting evidence for each idea.

### P05 · Human-LLM Compound System for Scientific Ideation through Facet Recombination and Novelty Evaluation

- **Authors and version:** Marissa Radensky et al.; arXiv preprint, v7 (2026-05-16); Scideator.
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2409.14634v7).
- **Review depth:** Selected full-text sections (`full_text_sections`).
- **Core contribution:** Organize papers and ideas using purpose, mechanism, and evaluation facets, and retrieve analogous papers at controlled conceptual distances.
- **Skill adaptation:** Recombine structured facets rather than merely swapping domain names. Track title changes across paper versions.

### P06 · Chain of Ideas: Revolutionizing Research Via Novel Idea Development with LLM Agents

- **Authors and version:** Long Li et al.; Findings of EMNLP 2025.
- **Primary source:** [Paper / official page](https://aclanthology.org/2025.findings-emnlp.477/).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Organize literature into chains of research development to show how successive methods address limitations, and introduce the Idea Arena evaluation protocol.
- **Skill adaptation:** Trace limitations and subsequent improvements in recent methods, and compare candidates at a consistent level of detail.

### P07 · MOOSE-Chem: Large Language Models for Rediscovering Unseen Chemistry Scientific Hypotheses

- **Authors and version:** Zonglin Yang et al.; ICLR 2025; arXiv v6 (2025-10-27).
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2410.07076v6).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Decompose hypothesis discovery into inspiration retrieval, hypothesis composition, and quality ranking, and evaluate rediscovery on a benchmark derived from 51 chemistry papers.
- **Skill adaptation:** Assess inspiration quality, composition logic, and ranking separately. Similarity-based rediscovery does not establish success in new experiments.

### P08 · Accelerating scientific discovery with Co-Scientist

- **Authors and version:** Juraj Gottweis et al.; Nature, published 2026-05-19.
- **Primary source:** [Paper / official page](https://www.nature.com/articles/s41586-026-10644-y).
- **Review depth:** Selected full-text sections (`full_text_sections`).
- **Core contribution:** Specialized roles generate, reflect on, rank, evolve, and cluster hypotheses, using tournament feedback and meta-review to improve subsequent search.
- **Skill adaptation:** Use bounded candidate evolution, deduplication, and consolidated critiques. Do not interpret Elo rankings as scientific truth.

### P09 · The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search

- **Authors and version:** Yutaro Yamada et al.; arXiv preprint, v1.
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2504.08066v1).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Connect hypothesis generation, experiments, analysis, and paper writing, using an experiment-management role and progressive tree search to explore proposals.
- **Skill adaptation:** Hand selected ideas over to small-scale experiments and preserve execution logs and unsuccessful branches.

### P10 · Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers

- **Authors and version:** Chenglei Si, Diyi Yang, Tatsunori Hashimoto; ICLR 2025.
- **Primary source:** [Paper / official page](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** In this controlled human evaluation, LLM-generated proposals were judged more novel but slightly weaker in feasibility.
- **Skill adaptation:** Assess novelty and feasibility separately, and avoid generalizing the finding to every research discipline.

### P11 · The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas

- **Authors and version:** Chenglei Si, Tatsunori Hashimoto, Diyi Yang; ICLR 2026; first posted to arXiv in 2025.
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2506.20803).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Forty-three experts executed randomly assigned ideas. Review scores for LLM-generated ideas declined more after execution, narrowing their initial advantage.
- **Skill adaptation:** Pair every central mechanism with a minimal discriminating experiment, refutation conditions, and a stopping rule.

### P12 · ResearchGym: Evaluating Language Model Agents on Real-World AI Research

- **Authors and version:** Aniketh Garikaparthi, Manasi Patwardhan, Arman Cohan; ICLR 2026 Agents in the Wild Workshop; arXiv v2.
- **Primary source:** [Paper / official page](https://arxiv.org/abs/2602.15112v2).
- **Review depth:** Abstract (`abstract`).
- **Core contribution:** Evaluate end-to-end research in containerized tasks with fixed data, evaluation procedures, and baselines, exposing reliability and resource-management problems in long-horizon execution.
- **Skill adaptation:** Freeze evaluation boundaries, prioritize small experiments with information value, and retain timeouts and failures.

### P13 · SciAgents: Automating Scientific Discovery Through Bioinspired Multi-Agent Intelligent Graph Reasoning

- **Authors and version:** Alireza Ghafarollahi, Markus J. Buehler; Advanced Materials 37, e2413523.
- **Primary source:** [Paper / official page](https://doi.org/10.1002/adma.202413523).
- **Review depth:** Original abstract located through primary-source search only (`primary_search_abstract_only`).
- **Core contribution:** Combine ontological knowledge graphs, language models, and multi-agent reasoning to explore interdisciplinary relationships in bioinspired materials.
- **Skill adaptation:** Optionally use concept and mechanism graphs to support cross-domain retrieval. A relationship alone does not establish causality or transferability.

## 3. Key tradeoffs

**Retrieval coverage and innovation distance.** Searching only within the target task can favor routine extensions; searching only distant domains can overlook close prior work. Read nearby work to establish the gap, search other settings through shared challenges, and then return to the target field to check for overlap (P01–P05). Semantic distance alone does not establish innovation: identify the consequential technical step missing from existing approaches.

**Generation diversity and executability.** Multiple generation routes can broaden the candidate pool, while tournament rankings and reviews may favor polished presentation. Deduplicate by technical operation, equalize comparison detail, and review resource and data assumptions separately (P04, P06, P08, P10). The budget tiers, candidate counts, and 0–4 rubric are engineering defaults of this skill, not universally optimal settings established by these papers.

**Proposal scores and practical utility.** IdeaScientist's main experiments compare research proposals. On the same backbone, its Base and Trained variants score 73.5 and 74.6 overall, versus 60.6 for DeepScientist. This comparison indicates a substantial workflow contribution; the additional RL gain should be distinguished from the workflow gain. P11 and P12 further show why hypothesis quality, resource management, implementation, and evaluation reliability matter during execution. Accordingly, distinguish `proposal_only`, `preliminary_validated`, and `independently_validated`, and attach refutation conditions to predictions.

**Controlled retrieval and memory contamination.** P01 and P07 use temporally controlled rediscovery designs, but a retrieval cutoff and knowledge stored in model parameters are different boundaries. Retrospective evaluation should hide target methods and results and report model-memory risks. Ordinary research searches should cover current literature.

**Role separation and genuine independence.** Specialized roles make intermediate artifacts inspectable. One model acting sequentially as several roles still does not constitute independent blind review. This skill supports one agent or optional independent roles and requires truthful reporting of independence. It does not require role retraining, a million-paper database, or a particular model.

## 4. Synthesis into this skill

1. Fix the question, inputs and outputs, resources, and evaluation contract.
2. Preserve actual search records and source evidence with locators.
3. Derive ordinary approaches from close prior work and freeze them before candidate generation.
4. Generate mechanisms through structural transfer, facet recombination, assumption changes, and simplification.
5. Assess novelty, grounding, soundness, feasibility, and testability separately.
6. Use minimal discriminating experiments to distinguish a new mechanism from simpler alternative explanations.
7. Preserve objections, rejected candidates, and the actual validation status.

This is an original workflow synthesis for local agents. Citations explain the design basis; the skill does not reproduce or distribute paper full texts, author code, or trained weights, and the combined workflow is not claimed to have undergone publication-level experimental validation.

## 5. Scope and limitations

Search the closest prior work for each new task. This review does not replace domain-expert verification or guarantee novelty. Abstract-level access supports only corresponding high-level claims; mechanism and novelty judgments should inspect the original methods.

P13's full text was inaccessible, so only its high-level design was checked through the original abstract in search results. Scideator uses different titles across versions; this review follows arXiv v7 while retaining the system name for retrieval.
