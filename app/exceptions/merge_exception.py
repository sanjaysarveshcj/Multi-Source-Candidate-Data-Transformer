from app.exceptions.base_exception import CandidateTransformerException


class MergeException(CandidateTransformerException):

    def __init__(self, message):

        super().__init__(
            message=message,
            status_code=500,
            error_code="MERGE_ERROR"
        )