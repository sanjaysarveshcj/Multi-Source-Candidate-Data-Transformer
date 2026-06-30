class ConfidenceEngine:

    SOURCE_CONFIDENCE = {
        "Recruiter CSV": 0.95,
        "Resume": 0.85
    }

    def score(self, source):

        return self.SOURCE_CONFIDENCE.get(source, 0.5)