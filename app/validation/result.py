from pydantic import BaseModel, Field


class ValidationResult(BaseModel):

    is_valid: bool = True

    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)

    score: float = 1.0