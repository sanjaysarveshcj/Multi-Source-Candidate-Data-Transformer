from app.validation.result import ValidationResult
from app.validation.rules import ValidationRules
from app.logging.logger import logger


class CandidateValidator:

    def validate(self, candidate):

        logger.info("Starting candidate validation...")

        result = ValidationResult()

        ValidationRules.validate_name(candidate, result)

        ValidationRules.validate_email(candidate, result)

        ValidationRules.validate_phone(candidate, result)

        ValidationRules.validate_skills(candidate, result)

        ValidationRules.validate_experience(candidate, result)

        ValidationRules.validate_education(candidate, result)

        if result.errors:

            result.is_valid = False

            logger.warning(
                f"Validation errors found: {result.errors}"
            )

        if result.warnings:

            logger.info(
                f"Validation warnings: {result.warnings}"
            )

        ##################################
        # Confidence Score
        ##################################

        deductions = (
            len(result.errors) * 0.2 +
            len(result.warnings) * 0.05
        )

        result.score = max(0.0, 1.0 - deductions)

        logger.info(
            f"Validation complete: valid={result.is_valid}, "
            f"score={result.score:.2f}, "
            f"{len(result.errors)} errors, "
            f"{len(result.warnings)} warnings"
        )

        return result