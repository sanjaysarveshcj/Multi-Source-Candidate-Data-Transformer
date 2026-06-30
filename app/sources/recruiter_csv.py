import pandas as pd

from typing import List

from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser
from app.logging.logger import logger
from app.exceptions.base_exception import CandidateTransformerException


class RecruiterCSVParser(SourceParser):

    def parse(self, source_path: str) -> List[RawCandidate]:

        logger.info(
            f"Parsing recruiter CSV: {source_path}"
        )

        try:
            df = pd.read_csv(source_path)
            logger.info(
                f"CSV loaded with {len(df)} rows"
            )

            # Heuristic column mapping
            headers = df.columns.tolist()
            # Normalize: lowercase, replace underscores and punctuation with spaces
            import re
            norm_headers = {h: re.sub(r'[^a-z0-9\s]', ' ', str(h).lower().replace('_', ' ')).strip() for h in headers}

            def find_match(*keywords):
                for h, nh in norm_headers.items():
                    words = set(nh.split())
                    for kw in keywords:
                        # Exact word match in the normalized header words
                        if kw in words:
                            return h
                return None

            mapping = {
                "full_name": find_match("name") or find_match("candidate", "applicant"),
                "headline": find_match("title", "role", "headline", "position"),
                "email": find_match("email", "e-mail"),
                "phone": find_match("phone", "mobile", "contact", "cell"),
                "city": find_match("city"),
                "region": find_match("state", "region", "province"),
                "country": find_match("country"),
                "location": find_match("location", "address"),
                "linkedin": find_match("linkedin"),
                "github": find_match("github"),
                "portfolio": find_match("portfolio", "website"),
                "skills": find_match("skill", "tech", "technologies"),
                "resume": find_match("resume", "description", "summary", "profile", "about"),
            }

            logger.info(f"Column mapping resolved: {mapping}")

            candidates = []
            
            for index, row in df.iterrows():

                def get_val(key):
                    col = mapping.get(key)
                    if col and col in row.index and pd.notna(row[col]):
                        return str(row[col])
                    return None

                full_name = get_val("full_name")
                headline = get_val("headline")
                email = get_val("email")
                phone = get_val("phone")

                # Extract location as structured dict
                location = {}
                city = get_val("city")
                region = get_val("region")
                country = get_val("country")
                loc_str = get_val("location")

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
                linkedin = get_val("linkedin")
                github = get_val("github")
                portfolio = get_val("portfolio")
                links = {
                    "linkedin": linkedin,
                    "github": github,
                    "portfolio": portfolio,
                    "other": [],
                }

                # Extract skills if available
                skills = []
                skills_str = get_val("skills")
                if skills_str:
                    skills = [
                        s.strip() for s in skills_str.split(",")
                        if s.strip()
                    ]
                
                # Fallback to extracting skills from "resume" field if available
                resume_text = get_val("resume")
                if not skills and resume_text:
                    import re
                    # Look for "Proficient in X, Y, Z"
                    match = re.search(r"Proficient in (.*?)(?:, with|\.)", resume_text, re.IGNORECASE)
                    if match:
                        skills_str = match.group(1)
                        skills = [s.strip() for s in skills_str.split(",") if s.strip()]

                candidates.append(RawCandidate(
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
                ))

            logger.info(f"CSV parsed successfully: {len(candidates)} candidates")
            return candidates

        except Exception as e:

            logger.error(
                f"Failed to parse recruiter CSV: {e}"
            )

            raise CandidateTransformerException(
                message=f"Failed to parse recruiter CSV: {e}",
                status_code=400,
                error_code="CSV_PARSE_ERROR",
            )