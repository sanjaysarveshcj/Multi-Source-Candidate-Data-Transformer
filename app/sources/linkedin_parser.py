import re

from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser
from app.logging.logger import logger


class LinkedInURLParser(SourceParser):
    """
    Parses a LinkedIn profile URL.

    Since LinkedIn does not expose a free public API,
    this parser extracts what it can from the URL itself
    (username / vanity slug) and constructs a minimal
    RawCandidate with the link preserved for downstream
    enrichment or manual review.

    Accepts:
        - Full URL:  "https://www.linkedin.com/in/john-doe-12345"
        - Short URL: "linkedin.com/in/johndoe"
    """

    LINKEDIN_PROFILE_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?linkedin\.com/in/([A-Za-z0-9_%\-]+)"
    )

    LINKEDIN_COMPANY_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?linkedin\.com/company/([A-Za-z0-9_%\-]+)"
    )

    ########################################################
    # Humanize slug → name heuristic
    ########################################################

    def _slug_to_name(self, slug: str) -> str:
        """
        Attempts to convert a LinkedIn vanity slug to
        a human-readable name.

        Examples:
            "john-doe-12345"  →  "John Doe"
            "jane_smith"      →  "Jane Smith"
        """

        # Strip trailing numeric IDs (common pattern)
        cleaned = re.sub(r"[-_]?\d{3,}$", "", slug)

        # Replace separators with spaces
        cleaned = re.sub(r"[-_]+", " ", cleaned)

        # Decode percent-encoding
        cleaned = cleaned.replace("%20", " ")

        # Title-case
        name = cleaned.strip().title()

        return name if name else slug

    ########################################################
    # Parse
    ########################################################

    def parse(self, source_path: str) -> RawCandidate:

        url = source_path.strip()

        logger.info(
            f"Parsing LinkedIn URL: {url}"
        )

        ####################################################
        # Extract profile slug
        ####################################################

        match = self.LINKEDIN_PROFILE_PATTERN.search(url)

        if not match:
            logger.warning(
                f"Could not extract LinkedIn username from: {url}"
            )
            return RawCandidate(
                source="LinkedIn",
                links={"linkedin": url, "github": None, "portfolio": None, "other": []},
            )

        slug = match.group(1)

        ####################################################
        # Build candidate
        ####################################################

        full_name = self._slug_to_name(slug)

        # Normalize the URL
        normalized_url = (
            f"https://www.linkedin.com/in/{slug}"
        )

        logger.info(
            f"LinkedIn profile parsed: {full_name} → {normalized_url}"
        )

        return RawCandidate(
            source="LinkedIn",
            full_name=full_name,
            emails=[],
            phones=[],
            skills=[],
            education=[],
            experience=[],
            links={
                "linkedin": normalized_url,
                "github": None,
                "portfolio": None,
                "other": [],
            },
        )
