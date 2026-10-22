# Research Ideation

**English** | [简体中文](README.zh-CN.md)

An evidence-grounded research ideation skill for local AI agents. Start with a research question and relevant literature, identify a scientific gap, develop hypotheses or methods, and produce a falsifiable validation plan.

The workflow supports computational research, experimental science, theoretical research, and observational studies in the social sciences. Use it to explore research directions, improve an idea, assess novelty, or design a study. It follows the portable `SKILL.md` format and works with a single agent or optional specialist roles. The host agent supplies the model and available research tools.

## Installation

Requirements: Git, Python 3.10+, and an agent that can read local skills.

```bash
git clone https://github.com/Alberto-Zhu/research-ideation.git
cd research-ideation
python tools/install_skill.py --agent codex
```

For Codex, the default destination is `~/.codex/skills/research-ideation`. If `CODEX_HOME` is set, the installer uses its `skills` directory instead. The Python commands work on Windows, Linux, and macOS. Reload your client's skills or start a new session after installation.

You can also install for Claude Code or choose a custom parent directory:

```bash
python tools/install_skill.py --agent claude
python tools/install_skill.py --dest /path/to/agent/skills
```

The installer refuses to overwrite an existing installation by default. With `--force`, it preserves the previous directory as a sibling backup before replacing it.

Alternatively, copy `skills/research-ideation` into your agent's skills directory. If your agent does not discover skills automatically, ask it to read the bundled `SKILL.md` directly. Automatic discovery depends on the client.

## Usage

```text
Use $research-ideation to develop research directions from my question and seed papers.
Search the closest prior work, identify evidence-supported gaps, generate six distinct
mechanisms or hypotheses, and shortlist two or three directions. Explain the novelty
delta, strongest objection, and falsifiable predictions. Choose an appropriate minimal
experiment, proof obligation, counterexample search, or observational design, and state
the resources, assumptions, and stopping rules.

Research question and constraints: …
```

To review an existing idea:

```text
Use $research-ideation to audit my idea. Check whether its central contribution can
be derived routinely from existing work, and design the cheapest discriminating test.
```

Choose `quick`, `standard`, or `deep` to control the search and revision budget. Offline runs can use supplied papers while explicitly recording coverage limits and unverified novelty.

## Workflow

1. Define the question, unresolved observation or failure case, resources, and evaluation contract.
2. Build a source ledger with page or section locators and an actual search log.
3. Identify supported gaps and freeze ordinary approaches derivable from prior work.
4. Generate distinct hypotheses or mechanisms through cross-domain transfer, facet recombination, and other routes.
5. Review novelty, grounding, soundness, feasibility, and testability separately.
6. Produce a minimal discriminating validation plan, refutation conditions, stopping rules, and an execution handoff.

Validation follows the research question: computational comparisons, controlled experiments, theoretical proofs and counterexamples, or observational identification. Unproven formulas, numerical bounds, and new claims must remain labeled as conjectures or derivation targets.

## Run artifacts and helper commands

| Artifact | Purpose |
|---|---|
| `run.json` | Contract, sources, gaps, candidates, reviews, and selection decisions |
| `report.md` | Readable research proposal |
| `search-log.jsonl` | Actual queries, dates, and retrieved source IDs |
| `baselines.lock.json` | Detect edits to frozen ordinary approaches |

The lock checks consistency; it does not establish true blinding or a trusted timestamp.

Initialize a run:

```bash
python skills/research-ideation/scripts/ideation.py init --out ./runs/demo --problem "Research question" --challenge "Unresolved challenge"
```

Have the agent fill the contract, evidence ledger, and ordinary approaches before freezing them. Generate candidates after the freeze:

```bash
python skills/research-ideation/scripts/ideation.py freeze-baselines --out ./runs/demo
```

Check a provisional draft or a completed proposal:

```bash
python skills/research-ideation/scripts/ideation.py validate --out ./runs/demo --stage draft
python skills/research-ideation/scripts/ideation.py validate --out ./runs/demo --stage final
```

Draft checks allow explicitly missing evidence while rejecting unknown citation IDs and structural inconsistencies. Final checks require completed evidence and review records. The scripts manage artifacts and check their structure; the host agent performs retrieval, reasoning, and writing.

## Research basis

The background review covers 13 core works, verified on **October 22, 2026**:

IdeaScientist; SciMON; ResearchAgent; SciPIP; Scideator; Chain of Ideas; MOOSE-Chem; Co-Scientist; The AI Scientist-v2; Can LLMs Generate Novel Research Ideas?; The Ideation–Execution Gap; ResearchGym; and SciAgents.

- [Literature Review and Method Comparison (English)](skills/research-ideation/references/literature-review.md)
- [文献综述与方法对照（中文版）](skills/research-ideation/references/literature-review.zh-CN.md)
- [Machine-readable bibliography](skills/research-ideation/references/bibliography.json)
- [Complete skill instructions](skills/research-ideation/SKILL.md)
- [Evaluation rubric](skills/research-ideation/references/evaluation.md)
- [Cross-disciplinary examples](skills/research-ideation/references/cross-domain-examples.md)

This is an original workflow synthesis informed by published research. It does not distribute paper full texts, author code, datasets, or model weights. The notes identify paper versions and review depth. The skill does not reproduce IdeaScientist's trained roles, million-paper corpus, or GRPO training. Its 0–4 rubric and budget settings are engineering defaults.

## Validation and limits

```bash
python -m unittest discover -s tests -v
```

Automated checks cover citation consistency, frozen-content changes, temporal cutoffs, review states, provisional drafts, theoretical evidence records, and installation protection.

Passing these checks establishes artifact consistency. Scientific correctness, global novelty, and practical value still require evidence and appropriate validation. Run artifacts and user inputs stay local by default; the utilities do not automatically upload them, publish them, call paid APIs, or train models.

## License

Original documentation and utility code are released under the [MIT License](LICENSE). Referenced works retain their respective rights.
