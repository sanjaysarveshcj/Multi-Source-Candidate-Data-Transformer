from app.logging.logger import logger


class EmailNormalizer:

    def normalize(self, emails):

        logger.info(
            f"Normalizing {len(emails)} emails..."
        )

        normalized = []

        seen = set()

        for email in emails:

            email = email.strip().lower()

            if email not in seen:

                seen.add(email)

                normalized.append(email)

        logger.info(
            f"Email normalization complete: "
            f"{len(normalized)} unique emails"
        )

        return normalized