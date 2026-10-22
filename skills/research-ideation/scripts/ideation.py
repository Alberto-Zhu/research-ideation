#!/usr/bin/env python3
"""Initialize and audit research-ideation artifacts; Python 3.10+, standard library."""
import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

DIMENSIONS = ("novelty", "grounding", "soundness", "feasibility", "testability")
ROLES = ("novelty", "feasibility", "adversarial")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(value):
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def initialize(out, problem, challenge, mode="online"):
    out = Path(out)
    if (out / "run.json").exists() or (out / "baselines.lock.json").exists():
        raise ValueError("Run artifacts already exist; choose a fresh directory.")
    out.mkdir(parents=True, exist_ok=True)
    template = Path(__file__).resolve().parents[1] / "assets" / "proposal-template.md"
    # Refuse to overwrite unrelated user artifacts as well.
    if any((out / p).exists() for p in ("report.md", "search-log.jsonl")):
        raise ValueError("Output directory already contains report/search artifacts.")
    run = {
        "schema_version": "1.0",
        "contract": {
            "problem": problem, "challenge": challenge, "constraints": [],
            "success_metric": "", "baseline": "", "evaluation_boundary": "",
            "budget": "standard", "access_mode": mode,
            "search_date": date.today().isoformat(), "search_coverage": "",
            "literature_cutoff": None
        },
        "sources": [], "gaps": [], "baseline_derivations": [], "ideas": [], "reviews": [],
        "selection": {"selected_ids": [], "rationale": "", "validation_status": "proposal_only",
                      "unresolved_risks": []}
    }
    write_json(out / "run.json", run)
    (out / "search-log.jsonl").write_text("", encoding="utf-8")
    (out / "report.md").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    return out / "run.json"


def freeze(out):
    out = Path(out)
    run = read_json(out / "run.json")
    if not isinstance(run, dict):
        raise ValueError("run.json must contain an object.")
    if run.get("ideas"):
        raise ValueError("Freeze ordinary solutions before creating candidates; use a new run for blinding.")
    baselines = run.get("baseline_derivations")
    if not isinstance(baselines, list) or len(baselines) < 2:
        raise ValueError("Provide at least two ordinary-solution derivations first.")
    lock = out / "baselines.lock.json"
    if lock.exists():
        raise ValueError("Baseline lock already exists; do not replace frozen derivations.")
    write_json(lock, {"frozen_at_utc": datetime.now(timezone.utc).isoformat(),
                     "sha256": digest(baselines), "baseline_derivations": baselines})
    return lock


def validate(out, stage="final"):
    out = Path(out)
    errors = []
    try:
        run = read_json(out / "run.json")
    except (OSError, ValueError) as exc:
        return [f"run.json: {exc}"]
    if not isinstance(run, dict):
        return ["run.json must contain an object."]
    final = stage == "final"

    def err(path, message):
        errors.append(f"{path}: {message}")

    def text(obj, key, path):
        value = obj.get(key)
        if not isinstance(value, str) or not value.strip():
            err(path + "." + key, "must be a nonempty string")
        return value

    def array(obj, key, path, minimum=0):
        value = obj.get(key)
        if not isinstance(value, list):
            err(path + "." + key, "must be an array")
            return []
        if len(value) < minimum:
            err(path + "." + key, f"requires at least {minimum} entries")
        return value

    def strings(obj, key, path, minimum=0):
        values = array(obj, key, path, minimum)
        for j, value in enumerate(values):
            if not isinstance(value, str) or not value.strip():
                err(f"{path}.{key}[{j}]", "must be a nonempty string")
        return values

    def objects(key):
        values = array(run, key, "run")
        good = []
        for j, value in enumerate(values):
            if not isinstance(value, dict):
                err(f"{key}[{j}]", "must be an object")
            else:
                good.append(value)
        return good

    def indexed(values, path):
        result = {}
        for j, value in enumerate(values):
            ident = text(value, "id", f"{path}[{j}]")
            if isinstance(ident, str) and ident.strip():
                if ident in result:
                    err(path, f"duplicate id {ident}")
                result[ident] = value
        return result

    if run.get("schema_version") != "1.0":
        err("schema_version", "expected 1.0")
    contract = run.get("contract")
    if not isinstance(contract, dict):
        err("contract", "must be an object")
        contract = {}
    if final:
        for k in ("problem", "challenge", "success_metric", "baseline",
                  "evaluation_boundary", "search_coverage"):
            text(contract, k, "contract")
        strings(contract, "constraints", "contract")
    if contract.get("access_mode") not in ("online", "offline"):
        err("contract.access_mode", "expected online or offline")
    if contract.get("budget") not in ("quick", "standard", "deep"):
        err("contract.budget", "expected quick, standard, or deep")
    for key in ("search_date", "literature_cutoff"):
        value = contract.get(key)
        if value is None and key == "literature_cutoff":
            continue
        try:
            date.fromisoformat(value)
        except (ValueError, TypeError):
            err("contract." + key, "expected YYYY-MM-DD or null for cutoff")
    cutoff = contract.get("literature_cutoff")

    sources = indexed(objects("sources"), "sources")
    for sid, src in sources.items():
        path = f"sources.{sid}"
        text(src, "title", path)
        url, local = src.get("url"), src.get("local_path")
        if not (isinstance(local, str) and local.strip()):
            if not (isinstance(url, str) and urlparse(url).scheme in ("https", "http")
                    and urlparse(url).netloc):
                err(path, "provide an http(s) URL or a local_path")
        year = src.get("year")
        if type(year) is not int or not 1800 <= year <= 2200:
            err(path + ".year", "expected an integer year")
        if src.get("access") not in ("full_text", "abstract", "metadata", "user_supplied"):
            err(path + ".access", "invalid access level")
        if type(src.get("inspected")) is not bool:
            err(path + ".inspected", "must be boolean")
        if src.get("inspected"):
            text(src, "locator", path)
            text(src, "finding", path)
            if cutoff is not None:
                pub = src.get("publication_date")
                try:
                    pd = date.fromisoformat(pub)
                    cd = date.fromisoformat(cutoff)
                    if pd > cd:
                        err(path, "inspected source is after the literature cutoff")
                except (ValueError, TypeError):
                    err(path + ".publication_date", "exact date required for retrospective use")

    def refs(values, path, full=False):
        if not isinstance(values, list):
            err(path, "must be an array of source IDs")
            return
        for sid in values:
            if not isinstance(sid, str) or sid not in sources:
                err(path, f"unknown source id {sid!r}")
                continue
            src = sources[sid]
            if final and not src.get("inspected"):
                err(path, f"{sid} has not been inspected")
            if final and full and src.get("access") not in ("full_text", "user_supplied"):
                err(path, f"{sid} requires full text for a mechanism-level gap")

    gaps = indexed(objects("gaps"), "gaps")
    for gid, gap in gaps.items():
        path = f"gaps.{gid}"
        text(gap, "claim", path)
        ids = strings(gap, "supporting_source_ids", path, 2 if final else 0)
        if final and len(set(v for v in ids if isinstance(v, str))) < 2:
            err(path, "gap needs two distinct supporting sources")
        refs(ids, path + ".supporting_source_ids", full=True)
        for j, item in enumerate(array(gap, "nearest_work", path, 2 if final else 0)):
            near = f"{path}.nearest_work[{j}]"
            if not isinstance(item, dict):
                err(near, "must be an object")
                continue
            refs([item.get("source_id")], near, full=True)
            text(item, "limitation", near)
            text(item, "evidence_locator", near)
        text(gap, "unresolved_assumption", path)

    baselines = objects("baseline_derivations")
    indexed(baselines, "baseline_derivations")
    for j, baseline in enumerate(baselines):
        path = f"baseline_derivations[{j}]"
        text(baseline, "mechanism", path)
        refs(strings(baseline, "source_ids", path, 1), path + ".source_ids")
        strings(baseline, "assumptions", path, 1)
        strings(baseline, "steps", path, 1)
    if final and len(baselines) < 2:
        err("baseline_derivations", "requires two ordinary solutions")
    lockpath = out / "baselines.lock.json"
    if lockpath.exists():
        try:
            lock = read_json(lockpath)
            if (not isinstance(lock, dict) or lock.get("sha256") != digest(baselines)
                    or lock.get("sha256") != digest(lock.get("baseline_derivations"))):
                err("baselines.lock.json", "frozen baseline digest mismatch")
        except (OSError, ValueError) as exc:
            err("baselines.lock.json", str(exc))
    elif final:
        err("baselines.lock.json", "missing; freeze before generating ideas")

    ideas = indexed(objects("ideas"), "ideas")
    if final and not gaps:
        err("gaps", "requires at least one supported gap")
    if final and not ideas:
        err("ideas", "requires at least one candidate, even if all are rejected")
    for iid, idea in ideas.items():
        path = f"ideas.{iid}"
        if not isinstance(idea.get("gap_id"), str) or idea.get("gap_id") not in gaps:
            err(path + ".gap_id", "unknown gap id")
        for key in ("title", "mechanism", "derivation_delta"):
            text(idea, key, path)
        refs(strings(idea, "source_ids", path, 1), path + ".source_ids")
        strings(idea, "assumptions", path, 1)
        if idea.get("status") not in ("candidate", "revise", "reject", "selected", "unvalidated"):
            err(path + ".status", "invalid status")
        for j, prior in enumerate(array(idea, "closest_prior_art", path, 1)):
            pp = f"{path}.closest_prior_art[{j}]"
            if not isinstance(prior, dict):
                err(pp, "must be an object")
                continue
            refs([prior.get("source_id")], pp)
            text(prior, "overlap", pp)
            text(prior, "non_obvious_delta", pp)
        for j, prediction in enumerate(array(idea, "predictions", path, 1)):
            pp = f"{path}.predictions[{j}]"
            if not isinstance(prediction, dict):
                err(pp, "must be an object")
                continue
            for key in ("claim", "metric", "comparator", "refutation_condition"):
                text(prediction, key, pp)
        ex = idea.get("validation_plan")
        if not isinstance(ex, dict):
            err(path + ".validation_plan", "must be an object")
        else:
            for key in ("minimal_test", "resources", "stop_rule"):
                text(ex, key, path + ".validation_plan")
            for key in ("baselines", "ablations", "validity_controls"):
                strings(ex, key, path + ".validation_plan", 1)
        transfer = idea.get("transfer")
        if transfer is not None:
            if not isinstance(transfer, dict):
                err(path + ".transfer", "must be an object or null")
            else:
                for key in ("source_setting", "target_setting", "shared_structure",
                            "adaptation", "boundary_condition"):
                    text(transfer, key, path + ".transfer")
        array(idea, "validation_evidence", path)

    latest = {}
    for j, review in enumerate(objects("reviews")):
        path = f"reviews[{j}]"
        iid, role = review.get("idea_id"), review.get("reviewer_role")
        if not isinstance(iid, str) or iid not in ideas:
            err(path + ".idea_id", "unknown idea id")
        if role not in ROLES:
            err(path + ".reviewer_role", "invalid role")
        if review.get("verdict") not in ("survive", "revise", "reject"):
            err(path + ".verdict", "invalid verdict")
        refs(strings(review, "evidence_source_ids", path, 1), path + ".evidence_source_ids")
        text(review, "objection", path)
        text(review, "response", path)
        scores = review.get("scores")
        if not isinstance(scores, dict):
            err(path + ".scores", "must be an object")
        else:
            for dimension in DIMENSIONS:
                value = scores.get(dimension)
                if type(value) is not int or not 0 <= value <= 4:
                    err(path + ".scores." + dimension, "expected integer 0–4")
        if isinstance(iid, str) and isinstance(role, str):
            latest[(iid, role)] = review

    selection = run.get("selection")
    if not isinstance(selection, dict):
        err("selection", "must be an object")
        selection = {}
    chosen = strings(selection, "selected_ids", "selection")
    if len(chosen) != len(set(v for v in chosen if isinstance(v, str))):
        err("selection.selected_ids", "duplicate idea IDs")
    if final:
        text(selection, "rationale", "selection")
        strings(selection, "unresolved_risks", "selection")
    status = selection.get("validation_status")
    if status not in ("proposal_only", "preliminary_validated", "independently_validated"):
        err("selection.validation_status", "invalid validation status")
    for iid in chosen:
        if not isinstance(iid, str) or iid not in ideas:
            err("selection.selected_ids", f"unknown idea id {iid!r}")
            continue
        if ideas[iid].get("status") != "selected":
            err("selection", f"{iid} must have status selected")
        if final:
            for role in ROLES:
                review = latest.get((iid, role))
                if not review or review.get("verdict") != "survive":
                    err("selection", f"{iid} needs a surviving {role} review")
                elif isinstance(review.get("scores"), dict):
                    if any(type(v) is int and v == 0 for v in review["scores"].values()):
                        err("selection", f"{iid} has a zero-scored gate in {role} review")
        if status in ("preliminary_validated", "independently_validated"):
            evidence = ideas[iid].get("validation_evidence", [])
            if not isinstance(evidence, list) or not evidence:
                err("selection", f"{iid} needs actual validation evidence for {status}")
            else:
                for j, item in enumerate(evidence):
                    if not isinstance(item, dict):
                        err(f"ideas.{iid}.validation_evidence[{j}]", "must be an object")
                    else:
                        text(item, "artifact", f"ideas.{iid}.validation_evidence[{j}]")
                        text(item, "result", f"ideas.{iid}.validation_evidence[{j}]")
    for iid, idea in ideas.items():
        if idea.get("status") == "selected" and iid not in chosen:
            err("selection", f"{iid} is marked selected but is absent from selected_ids")
    if status in ("preliminary_validated", "independently_validated") and not chosen:
        err("selection", "validated status requires a selected idea")

    logpath = out / "search-log.jsonl"
    if logpath.exists():
        for j, line in enumerate(logpath.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("expected object")
                for key in ("date", "query", "tool"):
                    text(row, key, f"search-log line {j}")
                refs(row.get("result_source_ids", []), f"search-log line {j}")
            except ValueError as exc:
                err(f"search-log line {j}", str(exc))
    elif final:
        err("search-log.jsonl", "missing")
    if final and not (out / "report.md").is_file():
        err("report.md", "missing")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--out", required=True)
    init.add_argument("--problem", required=True)
    init.add_argument("--challenge", required=True)
    init.add_argument("--mode", choices=("online", "offline"), default="online")
    lock = commands.add_parser("freeze-baselines")
    lock.add_argument("--out", required=True)
    check = commands.add_parser("validate")
    check.add_argument("--out", required=True)
    check.add_argument("--stage", choices=("draft", "final"), default="final")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            print(initialize(args.out, args.problem, args.challenge, args.mode))
        elif args.command == "freeze-baselines":
            print(freeze(args.out))
        else:
            errors = validate(args.out, args.stage)
            if errors:
                print("\n".join("ERROR " + e for e in errors), file=sys.stderr)
                return 1
            print("Artifact structure is consistent. Scientific validity and novelty require review.")
    except (OSError, ValueError) as exc:
        print("ERROR " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
