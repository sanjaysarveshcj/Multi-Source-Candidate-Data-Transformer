from app.extractors.resume_extractor import ResumeExtractor


def test_name_extraction():

    text = """
John Doe

Software Engineer

Email: john@gmail.com
"""

    extractor = ResumeExtractor()

    candidate = extractor.extract(text)

    assert candidate.full_name == "John Doe"

    assert "john@gmail.com" in candidate.emails