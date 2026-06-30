import pandas as pd

from app.models import Candidate
from app.sources.parser import SourceParser

class GithubParser(SourceParser):

    def parse(self, source_path: str):

        df = pd.read_csv(source_path)

        row = df.iloc[0]

        return Candidate(
            full_name="" if pd.isna(row.get("name")) else str(row.get("name")),
            phones=[] if pd.isna(row.get("phone")) else [str(row.get("phone"))],
            emails=[] if pd.isna(row.get("email")) else [str(row.get("email"))],
            headline="" if pd.isna(row.get("title")) else str(row.get("title")),
        )