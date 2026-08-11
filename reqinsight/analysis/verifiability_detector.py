class VerifiabilityDetector:
    """
    Detects technical criteria and explicit verification indicators
    within software requirements.
    """

    TECHNICAL_CRITERIA = [
        "tls",
        "bcrypt",
        "gdpr",
        "s3",
        "smtp",
        "api",
        "ssl",
        "https",
        "oauth",
        "jwt",
    ]

    VERIFICATION_TERMS = [
        "must support",
        "must allow",
        "must display",
        "must provide",
        "must perform",
        "must maintain",
        "must encrypt",
        "must comply",
        "must be able to",
    ]

    def detect(self, text):
        """
        Analyze a requirement and return detected
        verifiability indicators.
        """

        text_lower = text.lower()

        technical_criteria = [
            criterion
            for criterion in self.TECHNICAL_CRITERIA
            if criterion in text_lower
        ]

        verification_terms = [
            term
            for term in self.VERIFICATION_TERMS
            if term in text_lower
        ]

        return {
            "technical_criteria": technical_criteria,
            "verification_terms": verification_terms,
            "verifiable": bool(
                technical_criteria or verification_terms
            ),
        }