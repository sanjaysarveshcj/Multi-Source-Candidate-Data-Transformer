from app.logging.logger import logger


class ConfidenceEngine:

    SOURCE_CONFIDENCE = {
        "Recruiter CSV": 0.95,
        "Resume": 0.85,
        "LinkedIn": 0.70,
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