# Specialist contracts

Execute sequentially with one agent, or use isolated agents when delegation is supported
and permitted. Pass task-local files. Do not pass desired answers to reviewers.

| Role | Allowed input | Required output |
|---|---|---|
| Literature analyst | Contract, seeds, actual corpus/tools | Inspected sources, claim locators, search log, access limitations |
| Gap finder | Contract, target-setting prior work | 1–2 supported methodological gaps, near misses, assumptions |
| Ordinary-solution derivation | Contract and closest prior art only | 2–3 operational baselines; never show proposed ideas |
| Mechanism inventor | Contract, gaps, inspirations, frozen baselines | Diverse candidate cards with consequential deltas |
| Novelty auditor | Anonymous candidate, closest work, frozen baselines | Duplicate/derivability assessment and cited objection |
| Feasibility reviewer | Candidate and actual resources | Bottlenecks, cheaper pilot, meaningful comparator, stop rule |
| Adversarial reviewer | Candidate, evidence, experiment; initially omit other verdicts | Strongest competing explanation and discriminating test |
| Proposal writer | Surviving candidates, reviews, evidence, contract | report.md, run.json, honest validation status |

Require the inventor to explain source setting, shared structure, adaptation, and failure
boundary for analogies. Require reviewers to mark insufficient evidence as unassessed.
Require the writer to preserve rejected alternatives, missing evidence, and review
disagreement. Never invent datasets, source findings, results, or measured gains.
Claim independent review only when an independently scoped role actually ran.
