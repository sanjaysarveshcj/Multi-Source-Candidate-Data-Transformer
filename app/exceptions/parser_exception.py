from app.exceptions.base_exception import CandidateTransformerException


class ParserException(CandidateTransformerException):

    def __init__(self, message):

        super().__init__(
            message=message,
            status_code=400,
            error_code="PARSER_ERROR"
        )