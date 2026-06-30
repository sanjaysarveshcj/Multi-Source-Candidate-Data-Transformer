from app.sources.recruiter_csv import RecruiterCSVParser


def test_csv_parser(tmp_path):

    csv = tmp_path / "candidate.csv"

    csv.write_text(
        """candidate_id,full_name,headline,years_experience
1,John Doe,Software Engineer,5"""
    )

    parser = RecruiterCSVParser()

    candidate = parser.parse(csv)[0]

    assert candidate.full_name == "John Doe"
    assert candidate.headline == "Software Engineer"
    assert candidate.source == "Recruiter CSV"
    assert candidate.emails == []
    assert candidate.phones == []