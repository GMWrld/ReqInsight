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
        "must integrate",
        "must interface",
        "must be localized",
        "must have",
        "must include",
        "must contain",
        "must use",
        "must follow",
        "must respond",
        "must synchronize",
        "must upload",
        "must update",
        "must create",
        "must track",
        "must enable",
        "must assign",
        "must prioritize",
        "must analyze",
    ]

    NON_VERIFIABLE_TERMS = [
        "properly",
        "appropriately",
        "appropriate",
        "suitable",
        "easy",
        "efficiently",
        "efficient",
        "reliable",
        "useful",
        "satisfactory",
        "secure handling",
        "securely",
        "secure",
        "detailed",
        "prominently",
        "clear",
        "consistent",
        "user friendly",
        "user-friendly",
        "normal operating conditions",
        "peak usage",
        "low technical proficiency",
    ]

    SUBJECTIVE_TERMS = [
        "properly",
        "appropriately",
        "appropriate",
        "suitable",
        "easy to use",
        "easy",
        "user friendly",
        "user-friendly",
        "efficiently",
        "efficient",
        "reliable",
        "useful",
        "satisfactory",
        "secure handling",
        "securely",
        "secure",
        "detailed",
        "prominently",
        "clear error message",
        "consistent look and feel",
        "normal operating conditions",
        "peak usage",
        "low technical proficiency",
    ]

    def detect(self, text):
        """
        Analyze a requirement and return detected
        verifiability indicators.
        """

        text_lower = text.lower().strip()

        # ---------------------------------------------------------
        # 1. Detect technical criteria
        # ---------------------------------------------------------

        technical_criteria = [
            criterion
            for criterion in self.TECHNICAL_CRITERIA
            if criterion in text_lower
        ]

        # ---------------------------------------------------------
        # 2. Detect explicit verification terms
        # ---------------------------------------------------------

        verification_terms = [
            term
            for term in self.VERIFICATION_TERMS
            if term in text_lower
        ]

        # ---------------------------------------------------------
        # 3. Detect non-verifiable / subjective terminology
        # ---------------------------------------------------------

        non_verifiable_terms = [
            term
            for term in self.NON_VERIFIABLE_TERMS
            if term in text_lower
        ]

        subjective_terms = [
            term
            for term in self.SUBJECTIVE_TERMS
            if term in text_lower
        ]

        # ---------------------------------------------------------
        # 4. Detect objective indicators
        # ---------------------------------------------------------

        objective_indicators = [
            "must display",
            "must generate",
            "must send",
            "must allow",
            "must support",
            "must maintain",
            "must provide",
            "must store",
            "must validate",
            "must enforce",
            "must trigger",
            "must notify",
            "must encrypt",
            "must record",
            "must integrate",
            "shall display",
            "shall generate",
            "shall send",
            "shall allow",
            "shall support",
            "shall maintain",
            "shall provide",
            "shall store",
            "shall validate",
            "shall enforce",
            "shall trigger",
            "shall notify",
            "shall encrypt",
            "shall record",
            "shall integrate",
            "minimum",
            "maximum",
            "at least",
            "at most",
            "within",
            "format:",
            "specified",
            "defined",
            "threshold",
            "support",
            "allow",
            "enforce",
            "trigger",
            "encrypt",
            "generate",
            "send",
            "notify",
            "store",
            "record",
            "validate",
            "integrate",
            "assign",
            "prioritize",
            "maintain",
            "provide",
            "display",
            "upload",
            "update",
            "create",
            "track",
            "enable",
            "require",
            "follow",
            "analyze",
            "automatically",
            "must have",
            "must include",
            "must contain",
            "must use",
            "must follow",
            "must respond",
            "must synchronize",
            "must upload",
            "must update",
            "must create",
            "must track",
            "must enable",
            "must assign",
            "must prioritize",
            "must analyze",
            "responsive",
            "adaptable",
            "role-based access control",
            "rbac",
            "accessible",
            "icons",
            "shapes",
        ]

        objective_indicators_found = [
            indicator
            for indicator in objective_indicators
            if indicator in text_lower
        ]

        # ---------------------------------------------------------
        # 5. Strong verification terms
        # ---------------------------------------------------------
        #
        # These describe directly observable system behaviour.
        # They can remain verifiable even when the requirement
        # contains descriptive wording such as "clear".

        strong_verification_terms = [
            "must display",
            "must support",
            "must allow",
            "must encrypt",
            "must comply",
            "must be able to",
            "must integrate",
            "must interface",
            "must be localized",
        ]

        strong_verification_detected = [
            term
            for term in strong_verification_terms
            if term in text_lower
        ]

        # ---------------------------------------------------------
        # 6. Determine whether an objective acceptance criterion exists
        # ---------------------------------------------------------

        quantifiable_patterns = [
            "seconds",
            "second",
            "milliseconds",
            "millisecond",
            "minutes",
            "minute",
            "hours",
            "hour",
            "days",
            "day",
            "years",
            "year",
            "mb",
            "gb",
            "%",
            "minimum",
            "maximum",
            "at least",
            "at most",
            "within",
        ]

        quantifiable_indicators = [
            indicator
            for indicator in quantifiable_patterns
            if indicator in text_lower
        ]

        # Technical standards/frameworks are objective criteria.
        has_technical_criterion = bool(technical_criteria)

        # Explicit quantitative or acceptance criteria.
        has_strong_objective_criterion = bool(
            quantifiable_indicators
            or has_technical_criterion
        )

        # ---------------------------------------------------------
        # Determine verifiability
        # ---------------------------------------------------------

        if subjective_terms:
            if strong_verification_detected:
                verifiable = True
            else:
                verifiable = has_strong_objective_criterion
        else:
            verifiable = bool(
                technical_criteria
                or verification_terms
                or quantifiable_indicators
                or objective_indicators_found
            )

        # ---------------------------------------------------------
        # 7. Return analysis
        # ---------------------------------------------------------

        return {
            "technical_criteria": technical_criteria,
            "verification_terms": verification_terms,
            "non_verifiable_terms": non_verifiable_terms,
            "subjective_terms": subjective_terms,
            "objective_indicators": objective_indicators_found,
            "verifiable": verifiable,
        }