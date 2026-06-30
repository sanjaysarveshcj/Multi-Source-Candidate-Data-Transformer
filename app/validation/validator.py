from app.validation.result import ValidationResult
from app.validation.rules import ValidationRules


class CandidateValidator:

    def validate(self, candidate):

        result = ValidationResult()

        ValidationRules.validate_name(candidate, result)

        ValidationRules.validate_email(candidate, result)

        ValidationRules.validate_phone(candidate, result)

        ValidationRules.validate_skills(candidate, result)

        ValidationRules.validate_experience(candidate, result)

        ValidationRules.validate_education(candidate, result)

        if result.errors:

            result.is_valid = False

        ##################################
        # Confidence Score
        ##################################

        deductions = (
            len(result.errors) * 0.2 +
            len(result.warnings) * 0.05
        )

        result.score = max(0.0, 1.0 - deductions)

        return result