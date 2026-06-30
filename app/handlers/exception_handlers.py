from fastapi import Request
from fastapi.responses import JSONResponse

from app.logging.logger import logger
from app.exceptions.base_exception import CandidateTransformerException


async def candidate_exception_handler(
    request: Request,
    exc: CandidateTransformerException
):

    logger.error(
        f"{exc.error_code}: {exc.message}"
    )

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "success": False,

            "error": {

                "code": exc.error_code,

                "message": exc.message

            }

        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(exc)

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "error": {

                "code": "INTERNAL_SERVER_ERROR",

                "message": "Unexpected server error"

            }

        }
    )