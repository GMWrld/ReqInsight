class DocumentQualityScorer:
    """
    Calculates an overall quality score for an SRS document
    from individual requirement quality scores.
    """

    def calculate(self, requirement_results):
        """
        Calculate the arithmetic mean of all requirement scores.
        """

        if not requirement_results:
            return 0

        total_score = sum(
            result["score"]
            for result in requirement_results
        )

        return round(
            total_score / len(requirement_results),
            2
        )

    def classify(self, score):

        if score >= 90:
            return "EXCELLENT"

        if score >= 80:
            return "GOOD"

        if score >= 70:
            return "NEEDS REVIEW"

        return "POOR"

    def summarize(self, requirement_results):
        """
        Produce an overall quality summary for the SRS.
        """

        score = self.calculate(requirement_results)

        excellent = sum(
            1
            for result in requirement_results
            if result["classification"] == "EXCELLENT"
        )

        good = sum(
            1
            for result in requirement_results
            if result["classification"] == "GOOD"
        )

        needs_review = sum(
            1
            for result in requirement_results
            if result["classification"] == "NEEDS REVIEW"
        )

        poor = sum(
            1
            for result in requirement_results
            if result["classification"] == "POOR"
        )

        total = len(requirement_results)

        return {
            "score": score,
            "classification": self.classify(score),
            "total_requirements": total,
            "excellent": excellent,
            "good": good,
            "needs_review": needs_review,
            "poor": poor,
        }