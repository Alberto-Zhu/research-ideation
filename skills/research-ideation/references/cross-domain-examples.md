# Adapting the workflow across research disciplines

Treat every example as an unvalidated illustration. Retrieve the actual field literature
before asserting a gap or novelty. Match the validation method to the scientific claim.

## Computational methods

Question: can a data-selection rule remain useful when the downstream architecture changes?
Compare a proposed rule to strong simple selectors at equal data and compute budgets.
Hold out an architecture from tuning; remove the proposed causal component.
Refutation: any gain disappears under the matched simple comparator.
Evidence needed: current data-selection and transfer studies, inspected at method level.

## Experimental science

Question: which of two competing mechanisms could explain an observed plant stress response?
Map each mechanism to distinct observable consequences and a minimal controlled comparison.
Specify positive/negative controls, independent biological replicates, measurement limits,
and alternative explanations. Propose a design, not an invented biological result.
Refutation: the measurement that distinguishes the mechanisms contradicts the focal one.
Evidence needed: domain-specific primary studies and validated measurement procedures.

## Theoretical research

Question: can a stability bound for a class of graph processes be sharpened under a
precisely stated structural assumption?
State the conjecture, domain, assumptions, strongest known result, and proposed proof step.
Check limiting cases and search for counterexamples before a long proof attempt.
Refutation: an admissible counterexample or a step that requires an unavailable assumption.
Do not require a dataset split or measured improvement when the claim is mathematical.
Evidence needed: original theorems, exact assumptions, and proof dependencies.

## Observational and social science

Question: does an observed association between digital collaboration and task efficiency
reflect the tool's effect or differences in teams choosing it?
State the estimand, plausible confounding, identification assumptions, comparison group,
and falsification/negative-control checks. Plan sensitivity analysis.
Refutation: the proposed identification argument fails or results are explained by the
predeclared alternative. Do not infer causation from association alone.
Evidence needed: prior empirical designs, measurement validity, and contextual assumptions.

## Common handoff

In every track, state the unresolved question, closest evidence, consequential contribution,
strongest alternative, cheapest discriminating step, resources, and stop rule.
Use run.json's validation_plan for experiments, proofs, or observational checks.
Use validation_evidence only for actually obtained results, with artifact and result fields.
