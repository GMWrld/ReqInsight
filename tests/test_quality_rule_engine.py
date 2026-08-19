import unittest

from reqinsight.quality.quality_rule_engine import QualityRuleEngine


class TestQualityRuleEngine(unittest.TestCase):

    def setUp(self):
        self.engine = QualityRuleEngine()

    def test_should_modal_generates_warning(self):

        analysis = {
            "requirement_id": "FR-08",
            "modal_words": ["should"],
            "vague_terms": [],
            "quantifiable_constraints": [],
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0]["rule"],
            "MODAL-CONSISTENCY"
        )
        self.assertEqual(
            findings[0]["severity"],
            "WARNING"
        )

    def test_vague_term_generates_warning(self):

        analysis = {
            "requirement_id": "FR-01",
            "modal_words": ["must"],
            "vague_terms": ["user-friendly"],
            "quantifiable_constraints": [],
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0]["rule"],
            "VAGUE-TERM"
        )

    def test_nfr_without_measurement_generates_warning(self):

        analysis = {
            "requirement_id": "NFR-01",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": [],
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0]["rule"],
            "MEASURABILITY"
        )

    def test_measurable_nfr_passes(self):

        analysis = {
            "requirement_id": "NFR-01",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": ["2 seconds"],
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(findings, [])

    def test_good_requirement_passes(self):

        analysis = {
            "requirement_id": "FR-01",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": [],
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(findings, [])

    def test_nfr_with_concurrent_devices_passes(self):

        analysis = {
            "requirement_id": "NFR-01",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": ["10,000 concurrent devices"],
            "text": "Ingest data from at least 10,000 concurrent devices.",
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(findings, [])


    def test_nfr_with_minute_timeout_passes(self):

        analysis = {
            "requirement_id": "NFR-07",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": ["10-minute"],
            "text": "Enforce 10-minute inactivity timeout for clinical users.",
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(findings, [])


    def test_nfr_with_hours_constraint_passes(self):

        analysis = {
            "requirement_id": "NFR-10",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": ["24 hours"],
            "text": "The system must perform automated backups every 24 hours.",
        }

        findings = self.engine.evaluate(analysis)

        self.assertEqual(findings, [])


    def test_vague_requirement_is_not_automatically_measurability_issue(self):

        analysis = {
            "requirement_id": "NFR-11",
            "modal_words": ["must"],
            "vague_terms": ["clear"],
            "quantifiable_constraints": [],
            "text": (
                "The system must display a clear error message "
                "and allow the user to retry."
            ),
        }

        findings = self.engine.evaluate(analysis)

        rules = [finding["rule"] for finding in findings]

        self.assertIn("VAGUE-TERM", rules)
        self.assertNotIn("MEASURABILITY", rules)

    def test_non_verifiable_requirement_generates_verifiability_warning(self):

        analysis = {
            "requirement_id": "VER-001",
            "modal_words": ["should"],
            "vague_terms": ["properly"],
            "quantifiable_constraints": [],
            "text": "The system should work properly under normal operating conditions.",
        }

        findings = self.engine.evaluate(analysis)

        rules = [finding["rule"] for finding in findings]

        self.assertIn("VERIFIABILITY", rules)


    def test_verifiable_requirement_passes_verifiability_check(self):

        analysis = {
            "requirement_id": "VER-011",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": [],
            "text": "The system must display the patient's current heart rate on the dashboard.",
        }

        findings = self.engine.evaluate(analysis)

        rules = [finding["rule"] for finding in findings]

        self.assertNotIn("VERIFIABILITY", rules)


    def test_verifiable_localization_passes_verifiability_check(self):

        analysis = {
            "requirement_id": "NFR-09",
            "modal_words": ["must"],
            "vague_terms": [],
            "quantifiable_constraints": [],
            "text": "The system must be localized for English and Spanish languages.",
        }

        findings = self.engine.evaluate(analysis)

        rules = [finding["rule"] for finding in findings]

        self.assertNotIn("VERIFIABILITY", rules)


if __name__ == "__main__":
    unittest.main()