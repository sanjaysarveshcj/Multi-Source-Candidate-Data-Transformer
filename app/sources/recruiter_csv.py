import pandas as pd

from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser


class RecruiterCSVParser(SourceParser):

    def parse(self, source_path: str) -> RawCandidate:

        df = pd.read_csv(source_path)
        row = df.iloc[0]

        def get_value(*columns):
            for column in columns:
                if column in row.index and pd.notna(row[column]):
                    return str(row[column])
            return None

        full_name = get_value("full_name", "name")
        headline = get_value("headline", "title")
        email = get_value("email", "primary_email")
        phone = get_value("phone", "mobile")

        return RawCandidate(
            source="Recruiter CSV",
            full_name=full_name,
            headline=headline,
            emails=[] if email is None else [email],
            phones=[] if phone is None else [phone],
            skills=[],
            education=[],
            experience=[],
            links=[],
        )