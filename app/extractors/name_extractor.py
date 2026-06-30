from app.logging.logger import logger


class NameExtractor:
    """
    Extracts candidate name from the resume header.
    Assumption:
        First non-empty line of the resume is the candidate's name.
    """

    def extract(self, header: str):

        logger.info("Extracting candidate name from header...")

        lines = [
            line.strip()
            for line in header.split("\n")
            if line.strip()
        ]

        if not lines:
            logger.warning("No name found in header")
            return None

        name = lines[0]

        logger.info(f"Name extracted: {name}")

        return name