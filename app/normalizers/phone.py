import re

from app.logging.logger import logger

class PhoneNormalizer:
    """
    Normalizes phone numbers to E.164 format (+{country_code}{number}).
    Defaults to +1 (US) country code when not provided.
    """

    def normalize(self, phones):

        logger.info(
            f"Normalizing {len(phones)} phone numbers to E.164..."
        )

        result = []

        seen = set()

        for phone in phones:

            digits = re.sub(r"\D", "", phone)

            if not digits or len(digits) < 7:
                continue

            # If number has 10 digits, assume US (+1)
            if len(digits) == 10:
                digits = "1" + digits

            # If number has 11+ digits, assume country code is included
            # Ensure it starts with valid country code
            e164 = f"+{digits}"

            if e164 not in seen:

                seen.add(e164)

                result.append(e164)

        logger.info(
            f"Phone normalization complete: "
            f"{len(result)} unique numbers (E.164)"
        )

        return result