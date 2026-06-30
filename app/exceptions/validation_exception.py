from app.exceptions.base_exception import CandidateTransformerException


class ValidationException(CandidateTransformerException):

    def __init__(self, message):

        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR"
        )