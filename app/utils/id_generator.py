import hashlib

from app.logging.logger import logger


class CandidateIdGenerator:

    def generate(self, candidate):

        base = ""

        if candidate.full_name:
            base += candidate.full_name

        if candidate.emails:
            base += candidate.emails[0]

        if candidate.phones:
            base += candidate.phones[0]

        candidate_id = hashlib.md5(base.encode()).hexdigest()

        logger.info(
            f"Generated candidate ID: {candidate_id}"
        )

        return candidate_id