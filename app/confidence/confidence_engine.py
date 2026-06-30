from app.logging.logger import logger


class ConfidenceEngine:

    SOURCE_CONFIDENCE = {
        "Recruiter CSV": 0.95,
        "Resume": 0.85,
        "GitHub": 0.80,
        "ATS JSON": 0.90,
        "Text File": 0.75,
    }

    def score(self, source):

        score = self.SOURCE_CONFIDENCE.get(source, 0.5)

        logger.info(
            f"Confidence score for '{source}': {score}"
        )

        return score

    def skill_score(self, sources):
        """
        Compute skill confidence using independent-source probability:
            confidence = 1 - ∏(1 - source_confidence_i)

        Skills corroborated by more (or higher-trust) sources
        receive a higher confidence score.
        """

        if not sources:
            return 0.5

        product = 1.0

        for source in sources:

            source_conf = self.SOURCE_CONFIDENCE.get(source, 0.5)

            product *= (1.0 - source_conf)

        confidence = round(1.0 - product, 2)

        logger.info(
            f"Skill confidence from {sources}: {confidence}"
        )

        return confidence