import pandas as pd

from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser
from app.logging.logger import logger
from app.exceptions.base_exception import CandidateTransformerException


class RecruiterCSVParser(SourceParser):

    def parse(self, source_path: str) -> RawCandidate:

        logger.info(
            f"Parsing recruiter CSV: {source_path}"
        )

        try:

            df = pd.read_csv(source_path)

            logger.info(
                f"CSV loaded with {len(df)} rows"
            )

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

            # Extract location as structured dict
            location = {}
            city = get_value("city")
            region = get_value("state", "region")
            country = get_value("country")
            loc_str = get_value("location")

            if city or region or country:
                if city:
                    location["city"] = city
                if region:
                    location["region"] = region
                if country:
                    location["country"] = country
            elif loc_str:
                parts = [p.strip() for p in loc_str.split(",")]
                if len(parts) >= 1:
                    location["city"] = parts[0]
                if len(parts) >= 2:
                    location["region"] = parts[1]
                if len(parts) >= 3:
                    location["country"] = parts[2]

            # Extract links as structured dict
            linkedin = get_value("linkedin", "linkedin_url")
            github = get_value("github", "github_url")
            portfolio = get_value("portfolio", "website")
            links = {
                "linkedin": linkedin,
                "github": github,
                "portfolio": portfolio,
                "other": [],
            }

            # Extract skills if available
            skills = []
            skills_str = get_value("skills")
            if skills_str:
                skills = [
                    s.strip() for s in skills_str.split(",")
                    if s.strip()
                ]

            logger.info(
                f"CSV parsed successfully: {full_name}"
            )

            return RawCandidate(
                source="Recruiter CSV",
                full_name=full_name,
                headline=headline,
                location=location,
                emails=[] if email is None else [email],
                phones=[] if phone is None else [phone],
                skills=skills,
                education=[],
                experience=[],
                links=links,
            )

        except Exception as e:

            logger.error(
                f"Failed to parse recruiter CSV: {e}"
            )

            raise CandidateTransformerException(
                message=f"Failed to parse recruiter CSV: {e}",
                status_code=400,
                error_code="CSV_PARSE_ERROR",
            )