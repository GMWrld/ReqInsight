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


if __name__ == "__main__":
    unittest.main()