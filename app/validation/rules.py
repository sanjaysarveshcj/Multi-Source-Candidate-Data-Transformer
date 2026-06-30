import re

from app.logging.logger import logger


EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


class ValidationRules:

    @staticmethod
    def validate_name(candidate, result):

        if not candidate.full_name:

            logger.warning("Validation: Candidate name is missing")

            result.errors.append("Candidate name is missing")

    @staticmethod
    def validate_email(candidate, result):

        if not candidate.emails:

            logger.warning("Validation: No email found")

            result.warnings.append("No email found")
            return

        for email in candidate.emails:

            if not re.match(EMAIL_REGEX, email):

                logger.warning(
                    f"Validation: Invalid email: {email}"
                )

                result.errors.append(
                    f"Invalid email: {email}"
                )

    @staticmethod
    def validate_phone(candidate, result):

        if not candidate.phones:

            result.warnings.append(
                "No phone number found"
            )

    @staticmethod
    def validate_skills(candidate, result):

        if not candidate.skills:

            result.warnings.append(
                "No skills extracted"
            )

    @staticmethod
    def validate_experience(candidate, result):

        if not candidate.experience:

            result.warnings.append(
                "Experience section missing"
            )

    @staticmethod
    def validate_education(candidate, result):

        if not candidate.education:

            result.warnings.append(
                "Education section missing"
            )