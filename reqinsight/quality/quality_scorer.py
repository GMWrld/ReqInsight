class QualityScorer:
    """
    Calculates a quality score for an individual requirement
    based on the findings produced by the Quality Rule Engine.
    """

    STARTING_SCORE = 100

    PENALTIES = {
        "MODAL-CONSISTENCY": 15,
        "VAGUENESS": 15,
        "MEASURABILITY": 15,
        "VERIFIABILITY": 20,
    }

    def calculate(self, findings):
        """
        Calculate a quality score from a list of findings.
        """

        score = self.STARTING_SCORE

        for finding in findings:
            rule = finding.get("rule")

            penalty = self.PENALTIES.get(rule, 0)

            score -= penalty

        score = max(score, 0)

        return score

    def classify(self, score):
        """
        Convert a numeric quality score into a quality category.
        """

        if score >= 90:
            return "EXCELLENT"

        if score >= 80:
            return "GOOD"

        if score >= 70:
            return "NEEDS REVIEW"

        return "POOR"

    def score(self, findings):
        """
        Return both the numeric score and quality classification.
        """

        quality_score = self.calculate(findings)

        return {
            "score": quality_score,
            "classification": self.classify(quality_score),
        }