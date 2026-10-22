"""Synthetic fixtures validate artifact contracts, not any scientific claim."""
import copy
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(os.environ.get("RESEARCH_IDEATION_SKILL_PATH", ROOT / "skills" / "research-ideation"))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ideation = load_module("ideation", SKILL / "scripts" / "ideation.py")
installer = load_module("install_skill", ROOT / "tools" / "install_skill.py")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / "run"
        ideation.initialize(self.out, "Synthetic audit fixture", "Check contracts", "offline")
        self.run = ideation.read_json(self.out / "run.json")
        self.run["contract"].update(
            constraints=["One machine"], success_metric="Fixture consistency",
            baseline="Simple fixture baseline", evaluation_boundary="Fixed fixture split",
            search_coverage="Synthetic fixture only; no scientific evidence claimed")
        self.run["sources"] = [
            {"id": "S1", "title": "Synthetic source one", "url": "https://example.org/one",
             "year": 2024, "access": "full_text", "inspected": True,
             "locator": "Fixture section one", "finding": "Synthetic fixture statement"},
            {"id": "S2", "title": "Synthetic source two", "url": "https://example.org/two",
             "year": 2024, "access": "full_text", "inspected": True,
             "locator": "Fixture section two", "finding": "Synthetic fixture statement"}
        ]
        self.run["gaps"] = [{
            "id": "G1", "claim": "Synthetic fixture gap",
            "supporting_source_ids": ["S1", "S2"],
            "nearest_work": [
                {"source_id": "S1", "limitation": "Fixture limitation", "evidence_locator": "One"},
                {"source_id": "S2", "limitation": "Fixture limitation", "evidence_locator": "Two"}],
            "unresolved_assumption": "Synthetic assumption"}]
        self.run["baseline_derivations"] = [
            {"id": "B1", "mechanism": "Synthetic baseline one", "source_ids": ["S1"],
             "assumptions": ["Fixture assumption"], "steps": ["Fixture operation"]},
            {"id": "B2", "mechanism": "Synthetic baseline two", "source_ids": ["S2"],
             "assumptions": ["Fixture assumption"], "steps": ["Fixture operation"]}]
        self.save()
        ideation.freeze(self.out)
        self.run["ideas"] = [{
            "id": "I1", "gap_id": "G1", "title": "Synthetic candidate",
            "mechanism": "Synthetic operation", "source_ids": ["S1", "S2"],
            "derivation_delta": "Synthetic consequential difference",
            "closest_prior_art": [{"source_id": "S1", "overlap": "Fixture overlap",
                                  "non_obvious_delta": "Fixture difference"}],
            "assumptions": ["Fixture assumption"],
            "predictions": [{"claim": "Fixture prediction", "metric": "Fixture metric",
                             "comparator": "Fixture comparator",
                             "refutation_condition": "Fixture refuting observation"}],
            "validation_plan": {"minimal_test": "Synthetic fixture test",
                           "baselines": ["B1"], "ablations": ["Remove fixture operation"],
                           "validity_controls": ["Fixed fixture split"],
                           "resources": "No training", "stop_rule": "Stop after fixture"},
            "status": "selected", "validation_evidence": []}]
        self.run["reviews"] = [
            {"idea_id": "I1", "reviewer_role": role, "verdict": "survive",
             "evidence_source_ids": ["S1"], "objection": "Synthetic objection",
             "response": "Synthetic response", "scores": {k: 3 for k in ideation.DIMENSIONS}}
            for role in ideation.ROLES]
        self.run["selection"].update(selected_ids=["I1"], rationale="Synthetic fixture selection",
                                     unresolved_risks=["Fixture is not science"])
        self.save()

    def save(self):
        ideation.write_json(self.out / "run.json", self.run)

    def errors(self):
        self.save()
        return ideation.validate(self.out, "final")

    def test_valid_structure(self):
        self.assertEqual(self.errors(), [])

    def test_unknown_citation(self):
        self.run["ideas"][0]["source_ids"] = ["MISSING"]
        self.assertTrue(any("unknown source" in e for e in self.errors()))

    def test_frozen_content_change(self):
        self.run["baseline_derivations"][0]["mechanism"] = "Changed after generation"
        self.assertTrue(any("digest mismatch" in e for e in self.errors()))

    def test_freeze_after_candidate_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "before creating candidates"):
            ideation.freeze(self.out)

    def test_lock_cannot_be_replaced(self):
        self.run["ideas"] = []
        self.save()
        with self.assertRaisesRegex(ValueError, "already exists"):
            ideation.freeze(self.out)

    def test_gap_requires_full_text(self):
        self.run["sources"][0]["access"] = "abstract"
        self.assertTrue(any("requires full text" in e for e in self.errors()))

    def test_unread_source_cannot_support_final_idea(self):
        self.run["sources"][0]["inspected"] = False
        self.assertTrue(any("not been inspected" in e for e in self.errors()))

    def test_boolean_is_not_a_score(self):
        self.run["reviews"][0]["scores"]["novelty"] = True
        self.assertTrue(any("integer" in e for e in self.errors()))

    def test_selected_requires_three_roles(self):
        self.run["reviews"].pop()
        self.assertTrue(any("adversarial review" in e for e in self.errors()))

    def test_latest_rejection_blocks_selection(self):
        review = copy.deepcopy(self.run["reviews"][0])
        review["verdict"] = "reject"
        self.run["reviews"].append(review)
        self.assertTrue(any("surviving novelty review" in e for e in self.errors()))

    def test_validated_label_requires_measurements(self):
        self.run["selection"]["validation_status"] = "preliminary_validated"
        self.assertTrue(any("actual validation evidence" in e for e in self.errors()))

    def test_theoretical_validation_uses_proof_artifacts(self):
        self.run["contract"]["evaluation_boundary"] = "Exact proposition and assumptions"
        self.run["ideas"][0]["validation_plan"]["minimal_test"] = "Proof and counterexample checks"
        self.run["selection"]["validation_status"] = "independently_validated"
        artifact = self.out / "synthetic-proof.txt"
        artifact.write_text("Synthetic fixture only, not a scientific result.", encoding="utf-8")
        self.run["ideas"][0]["validation_evidence"] = [
            {"artifact": str(artifact), "result": "Fixture proposition checked"}]
        self.assertEqual(self.errors(), [])

    def test_cutoff_requires_exact_dates(self):
        self.run["contract"]["literature_cutoff"] = "2025-01-01"
        self.assertTrue(any("exact date required" in e for e in self.errors()))

    def test_post_cutoff_source_is_rejected(self):
        self.run["contract"]["literature_cutoff"] = "2025-01-01"
        for source in self.run["sources"]:
            source["publication_date"] = "2026-01-01"
        self.assertTrue(any("after the literature cutoff" in e for e in self.errors()))

    def test_malformed_identifiers_produce_errors(self):
        self.run["ideas"][0]["gap_id"] = []
        self.run["reviews"][0]["idea_id"] = []
        self.assertTrue(self.errors())

    def test_zero_finalists_is_valid(self):
        self.run["ideas"][0]["status"] = "reject"
        self.run["selection"]["selected_ids"] = []
        for review in self.run["reviews"]:
            review["verdict"] = "reject"
        self.assertEqual(self.errors(), [])

    def test_existing_run_is_preserved(self):
        before = (self.out / "run.json").read_bytes()
        with self.assertRaises(ValueError):
            ideation.initialize(self.out, "Other", "Other")
        self.assertEqual((self.out / "run.json").read_bytes(), before)


class InstallationTests(unittest.TestCase):
    def test_install_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / "skills"
            target, backup = installer.install(SKILL, parent)
            self.assertIsNone(backup)
            marker = target / "user-marker.txt"
            marker.write_text("Keep me", encoding="utf-8")
            with self.assertRaises(ValueError):
                installer.install(SKILL, parent)
            self.assertEqual(marker.read_text(encoding="utf-8"), "Keep me")
            target, backup = installer.install(SKILL, parent, force=True)
            self.assertTrue((backup / "user-marker.txt").exists())
            self.assertFalse((target / "user-marker.txt").exists())
            self.assertEqual((target / "SKILL.md").read_bytes(), (SKILL / "SKILL.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
