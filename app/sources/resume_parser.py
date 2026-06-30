# pyrefly: ignore [missing-import]
import pdfplumber

from app.logging.logger import logger
from app.exceptions.base_exception import CandidateTransformerException


class ResumePDFParser:

    def parse(self, pdf_path: str) -> str:

        logger.info(
            f"Parsing resume PDF: {pdf_path}"
        )

        try:

            text = ""

            with pdfplumber.open(pdf_path) as pdf:

                logger.info(
                    f"PDF opened with {len(pdf.pages)} pages"
                )

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            logger.info(
                f"Resume PDF parsed: {len(text)} characters extracted"
            )

            return text.strip()

        except Exception as e:

            logger.error(
                f"Failed to parse resume PDF: {e}"
            )

            raise CandidateTransformerException(
                message=f"Failed to parse resume PDF: {e}",
                status_code=400,
                error_code="RESUME_PARSE_ERROR",
            )