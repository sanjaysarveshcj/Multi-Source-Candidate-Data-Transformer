# pyrefly: ignore [missing-import]
import pytest

from app.sources.linkedin_parser import LinkedInURLParser


class TestLinkedInURLParser:

    def setup_method(self):
        self.parser = LinkedInURLParser()

    ####################################################
    # Slug to name conversion
    ####################################################

    def test_slug_to_name_with_numeric_suffix(self):
        name = self.parser._slug_to_name("john-doe-12345")
        assert name == "John Doe"

    def test_slug_to_name_simple(self):
        name = self.parser._slug_to_name("janedoe")
        assert name == "Janedoe"

    def test_slug_to_name_with_underscores(self):
        name = self.parser._slug_to_name("jane_smith")
        assert name == "Jane Smith"

    def test_slug_to_name_with_hyphens(self):
        name = self.parser._slug_to_name("sanjay-sarvesh")
        assert name == "Sanjay Sarvesh"

    ####################################################
    # Full URL parsing
    ####################################################

    def test_parse_full_url(self):

        result = self.parser.parse(
            "https://www.linkedin.com/in/john-doe-12345"
        )

        assert result.source == "LinkedIn"
        assert result.full_name == "John Doe"
        assert (
            "https://www.linkedin.com/in/john-doe-12345"
            in result.links
        )

    def test_parse_short_url(self):

        result = self.parser.parse(
            "linkedin.com/in/sanjay-sarvesh"
        )

        assert result.source == "LinkedIn"
        assert result.full_name == "Sanjay Sarvesh"

    def test_parse_invalid_url(self):

        result = self.parser.parse(
            "https://example.com/not-linkedin"
        )

        assert result.source == "LinkedIn"
        assert result.full_name is None
        assert len(result.links) == 1

    def test_parse_preserves_link(self):

        result = self.parser.parse(
            "https://www.linkedin.com/in/dev-engineer"
        )

        assert any(
            "linkedin.com" in link
            for link in result.links
        )

    ####################################################
    # Edge cases
    ####################################################

    def test_parse_empty_string(self):

        result = self.parser.parse("")

        assert result.source == "LinkedIn"
        assert result.full_name is None

    def test_parse_strips_whitespace(self):

        result = self.parser.parse(
            "  https://www.linkedin.com/in/test-user  "
        )

        assert result.full_name == "Test User"
