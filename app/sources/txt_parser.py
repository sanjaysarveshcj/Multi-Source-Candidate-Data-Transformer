from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser
from app.extractors.resume_extractor import ResumeExtractor
from app.logging.logger import logger


class TxtFileParser(SourceParser):
    """
    Parses a plain text (.txt) file containing candidate
    information. Reuses the ResumeExtractor to extract
    structured data from unstructured text.

    This is similar to the resume parser but works with
    raw .txt files instead of PDFs.
    """

    def __init__(self):

        self.extractor = ResumeExtractor()

    ########################################################
    # Read text from file path or raw string
    ########################################################

    def _read_text(self, source: str) -> str:

        source = source.strip()

        # Try reading as a file path
        try:
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        except (FileNotFoundError, OSError):
            pass

        # Try with latin-1 encoding
        try:
            with open(source, "r", encoding="latin-1") as f:
                return f.read()
        except (FileNotFoundError, OSError):
            pass

        # If it's long enough, treat as raw text content
        if len(source) > 100:
            return source

        raise FileNotFoundError(
            f"Cannot read text file: {source}"
        )

    ########################################################
    # Main parse method
    ########################################################

    def parse(self, source_path: str) -> RawCandidate:

        logger.info(
            f"Parsing TXT file: {source_path}"
        )

        text = self._read_text(source_path)

        if not text.strip():
            logger.warning(
                "TXT file is empty, returning empty candidate"
            )
            return RawCandidate(source="Text File")

        ####################################################
        # Reuse ResumeExtractor for structured extraction
        ####################################################

        candidate = self.extractor.extract(text)

        # Override source label
        candidate.source = "Text File"

        logger.info(
            f"TXT file parsed: {candidate.full_name} "
            f"({len(candidate.skills)} skills, "
            f"{len(candidate.experience)} experience entries)"
        )

        return candidate
