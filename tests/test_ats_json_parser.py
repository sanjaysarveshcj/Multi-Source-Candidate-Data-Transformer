# pyrefly: ignore [missing-import]
import pytest
import json
import os
import tempfile

from app.sources.ats_json_parser import ATSJsonParser


class TestATSJsonParser:

    def setup_method(self):
        self.parser = ATSJsonParser()

    ####################################################
    # Parse nested JSON (with "candidate" wrapper)
    ####################################################

    def test_parse_nested_json_string(self):

        data = json.dumps({
            "candidate": {
                "first_name": "Sanjay",
                "last_name": "Sarvesh",
                "email": "sanjay@example.com",
                "phone": "+91-9876543210",
                "headline": "Full Stack Developer",
                "skills": ["Python", "FastAPI"],
                "experience": [
                    {
                        "company": "TechCorp",
                        "title": "Engineer",
                        "start_date": "2022-01",
                        "end_date": "2025-06",
                    }
                ],
                "education": [
                    {
                        "institution": "MIT",
                        "degree": "B.Tech",
                        "field_of_study": "CS",
                        "end_year": 2020,
                    }
                ],
            }
        })

        result = self.parser.parse(data)

        assert result.source == "ATS JSON"
        assert result.full_name == "Sanjay Sarvesh"
        assert "sanjay@example.com" in result.emails
        assert "+91-9876543210" in result.phones
        assert "Python" in result.skills
        assert len(result.experience) == 1
        assert result.experience[0]["company"] == "TechCorp"
        assert len(result.education) == 1

    ####################################################
    # Parse flat JSON (no "candidate" wrapper)
    ####################################################

    def test_parse_flat_json(self):

        data = json.dumps({
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "skills": ["React", "Node.js"],
        })

        result = self.parser.parse(data)

        assert result.full_name == "Jane Doe"
        assert "jane@example.com" in result.emails
        assert "React" in result.skills

    ####################################################
    # Parse from file
    ####################################################

    def test_parse_from_file(self):

        data = {
            "candidate": {
                "full_name": "File Candidate",
                "email": "file@test.com",
            }
        }

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        ) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            result = self.parser.parse(temp_path)
            assert result.full_name == "File Candidate"
            assert "file@test.com" in result.emails
        finally:
            os.unlink(temp_path)

    ####################################################
    # Name extraction fallback
    ####################################################

    def test_name_from_first_last(self):

        data = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
        })

        result = self.parser.parse(data)
        assert result.full_name == "John Doe"

    def test_name_fallback_to_name_field(self):

        data = json.dumps({
            "name": "Single Name Field",
        })

        result = self.parser.parse(data)
        assert result.full_name == "Single Name Field"

    ####################################################
    # Location extraction
    ####################################################

    def test_location_from_parts(self):

        data = json.dumps({
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
        })

        result = self.parser.parse(data)
        assert "Chennai" in result.location
        assert "India" in result.location

    ####################################################
    # Social profiles → links
    ####################################################

    def test_social_profiles_extracted(self):

        data = json.dumps({
            "social_profiles": [
                {"url": "https://github.com/test"},
                {"url": "https://linkedin.com/in/test"},
            ]
        })

        result = self.parser.parse(data)
        assert "https://github.com/test" in result.links
        assert "https://linkedin.com/in/test" in result.links

    ####################################################
    # Tags merged with skills
    ####################################################

    def test_tags_merged_with_skills(self):

        data = json.dumps({
            "skills": ["Python"],
            "tags": ["backend", "api"],
        })

        result = self.parser.parse(data)
        assert "Python" in result.skills
        assert "backend" in result.skills
        assert "api" in result.skills

    ####################################################
    # Edge: email as list
    ####################################################

    def test_email_as_list(self):

        data = json.dumps({
            "email": ["a@test.com", "b@test.com"],
        })

        result = self.parser.parse(data)
        assert "a@test.com" in result.emails
        assert "b@test.com" in result.emails

    ####################################################
    # Edge: applicant wrapper
    ####################################################

    def test_applicant_wrapper(self):

        data = json.dumps({
            "applicant": {
                "full_name": "Applicant Wrapper",
            }
        })

        result = self.parser.parse(data)
        assert result.full_name == "Applicant Wrapper"
