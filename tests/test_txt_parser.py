# pyrefly: ignore [missing-import]
import pytest
import os
import tempfile

from app.sources.txt_parser import TxtFileParser


class TestTxtFileParser:

    def setup_method(self):
        self.parser = TxtFileParser()

    ####################################################
    # Parse from file
    ####################################################

    def test_parse_txt_file(self):

        content = (
            "John Doe\n"
            "john@example.com | 9876543210\n"
            "https://github.com/johndoe\n\n"
            "SKILLS\n"
            "Python, Java, Docker\n\n"
            "EXPERIENCE\n"
            "Software Engineer at TechCorp\n"
            "Jan 2020 - Dec 2023\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)[0]

            assert result.source == "Text File"
            assert result.full_name is not None

        finally:
            os.unlink(temp_path)

    ####################################################
    # Empty file
    ####################################################

    def test_parse_empty_file(self):

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write("")
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)[0]

            assert result.source == "Text File"

        finally:
            os.unlink(temp_path)

    ####################################################
    # Source label
    ####################################################

    def test_source_label_is_text_file(self):

        content = "Jane Doe\njane@example.com\n"

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)[0]
            assert result.source == "Text File"
        finally:
            os.unlink(temp_path)

    ####################################################
    # File not found
    ####################################################

    def test_parse_nonexistent_file_raises(self):

        with pytest.raises(FileNotFoundError):
            self.parser.parse("/nonexistent/path.txt")
