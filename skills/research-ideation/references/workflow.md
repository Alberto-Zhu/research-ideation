# Workflow and artifact contracts

## Contents

1. Contract
2. Search and evidence
3. Gaps and frozen baselines
4. Mechanisms
5. Review
6. Validation tracks
7. Offline and retrospective use
8. Structured artifacts

## 1. Contract

Record `problem, challenge, constraints, success_metric, baseline, evaluation_boundary,
budget, access_mode, search_date, search_coverage, literature_cutoff`.
Translate broad goals into a scientific question, required explanation or result,
and unresolved observation. Use input/output when appropriate to the task.
State which variables may change. Distinguish the application from the research object.
Use a measurable success criterion without inventing an expected gain.
Set literature_cutoff to null for ordinary current research.

## 2. Search and evidence

Use available search tools, scholarly APIs, local PDFs, or a supplied corpus.
Require no paid API. Search four families:
- Exact problem + failure axis, including alternate terminology.
- Closest mechanism + variants and simpler alternatives.
- The same challenge in another setting.
- Negative results, limitations, replications, and confounders.

For standard mode, aim for 3–5 closest works, 2–4 inspirations, 2 evaluation or
execution studies, and relevant task benchmarks. Groups may overlap.
Record inaccessible texts and coverage limits; do not simulate searches.

Source fields: `id, title, url or local_path, year, publication_date (when known),
access, inspected, locator, finding`.
Use access `full_text, abstract, metadata, user_supplied`.
Use page/section locators for mechanism claims. A URL alone is not evidence.
Preserve canonical paper identifiers separately from run-local IDs such as S01.
Keep reported evidence, author speculation, and your inference distinguishable.

Record one JSON object per actual query in search-log.jsonl:
`{"date":"YYYY-MM-DD","query":"...","tool":"...","result_source_ids":["S01"],"note":"..."}`.
Treat data downloads and code execution as separate authorized tasks.

## 3. Gaps and frozen baselines

Write one or two gaps with supporting source IDs, near-miss methods, specific
limitations/locators, and an unresolved assumption. Require two distinct read sources.
Use full text for methodological claims. A missing benchmark is an evaluation
contribution until a new mechanism or scientific insight is established.

Before seeing new ideas, derive 2–3 ordinary approaches from close prior art.
Record source IDs, assumptions, and operational steps. Run freeze-baselines.
If candidates already exist, do not manufacture a blinded derivation afterward:
use a fresh independent context, or report that the comparison is post hoc.

## 4. Mechanisms

Explore transfer of decision rules, invariances, abstractions, or resource allocation;
recombination of purpose/mechanism/evaluation facets; justified assumption changes;
and simpler sufficient statistics or operations.

Use the argument: failure F follows from assumption A; operation M changes quantity Q;
therefore predict outcome O under condition C.
A list of model names is insufficient.

For each closest work record shared operation, consequential new operation, and the
evidence needed. Examine whether more compute, labels, data, a larger model, or ordinary
tuning could explain the predicted advantage.
Record parent_id when evolving an idea rather than overwriting its history.

## 5. Review

Run novelty, feasibility, and adversarial passes separately.
Give the novelty reviewer frozen derivations and the closest sources.
Give the feasibility reviewer the actual resources and data constraints.
Ask the adversarial reviewer for the strongest competing explanation and its test.
Use uniform candidate detail and equal retrieval budgets.

Anonymous pairwise comparisons can aid selection. Elo and LLM scores are ordinal
workflow aids, not calibrated probabilities of success or acceptance.
Swap order on close cases; preserve ties and disagreement.
Revise only when the objection is actionable. Stop at the configured cap or when
iterations add terminology without a new operation.

## 6. Validation tracks

Choose a track before selecting methods. For computational work, use fixed evaluation
data and resource controls. For laboratory work, define controls, independent replicates,
measurement validity, and a discriminating observable. For theory, state the conjecture,
proof obligations, exact assumptions, comparison theorem, limiting cases, and counterexample
search. For observational work, define the estimand, identification assumptions, confounding,
sensitivity analyses, and negative controls. Do not force train/test partitions onto
non-computational work. Interpret baselines as comparison theories or control conditions,
ablations as assumption removal when appropriate, and validity_controls as threats to inference.

Plan: establish the baseline; run the cheapest falsification test; compare matched
alternatives; remove the causal component; test a held-out domain/architecture if
transfer is claimed.

Specify the independent unit (patient, machine, production batch, dataset).
Split before tuning. Prevent test feedback from changing selection, reward, prompts,
stopping rules, or hyperparameters. Use validation for selection.
Report uncertainty when informative and include boundary/failure cases.

Estimate person time, GPU time, external cost, and dependencies with explicit assumptions.
Prefer a pilot whose result changes the decision. Distinguish proposal-only,
preliminary_validated, and independently_validated status. Attach real evidence for stronger labels.

## 7. Offline and retrospective use

Offline: use inspected supplied material, name the corpus boundary, and mark novelty
coverage incomplete. Bundled background literature is not a current task-specific search.
Use validate --stage draft for provisional work: empty evidence lists are allowed, while
unknown source IDs and structural contradictions still fail. Final validation requires
completed evidence. Label unproved numerical bounds, formulas, and proposed baselines
as conjectures or derivation targets, not established results.

Retrospective: filter by publication date, not ingestion. Hide target methods/results
from the proposing context. Separate tasks by source paper and shared problem identity.
A retrieval cutoff does not establish a model's parametric knowledge cutoff.
Audit reconstructed inputs for method clues and report residual contamination.

## 8. Structured artifacts

Use the initializer for run.json. The authoritative fields are `contract, sources,
gaps, baseline_derivations, ideas, reviews, selection`. Extra task-specific fields
are permitted.

Each gap: `id, claim, supporting_source_ids, nearest_work, unresolved_assumption`.
Each near miss: `source_id, limitation, evidence_locator`.
Each baseline: `id, mechanism, source_ids, assumptions, steps`.
Each idea: `id, gap_id, title, mechanism, source_ids, derivation_delta, closest_prior_art,
assumptions, predictions, validation_plan, status, validation_evidence`.
Each prior-art comparison: `source_id, overlap, non_obvious_delta`.
Optional transfer: `source_setting, target_setting, shared_structure, adaptation,
boundary_condition`.
Each prediction: `claim, metric, comparator, refutation_condition`.
Each validation plan: `minimal_test, baselines, ablations, validity_controls, resources,
stop_rule`.

Each review: `idea_id, reviewer_role, verdict, evidence_source_ids, objection, response,
scores`. Use roles novelty/feasibility/adversarial and verdicts survive/revise/reject.
Use the five dimensions in evaluation.md, with integer scores 0–4.
For an idea/role pair, the latest review supersedes earlier ones; preserve the history.
Selected ideas require all three roles and no unresolved non-survive verdict.
Use no selected ideas when none survive.

The checker is local: it does not fetch sources, judge entailment, or establish blinding.

Each validation evidence item contains `artifact` and `result`. A result may be a measured
observation, a computational outcome, a proof, an independent proof check, or a counterexample.
