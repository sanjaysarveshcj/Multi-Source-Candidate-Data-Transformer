import json
from typing import List

from app.models.raw_candidate import RawCandidate
from app.sources.parser import SourceParser
from app.logging.logger import logger


class ATSJsonParser(SourceParser):
    """
    Parses an ATS (Applicant Tracking System) JSON blob
    into a RawCandidate.

    Supports two input modes:
        1. A file path to a .json file
        2. A raw JSON string

    Expected JSON structure (flexible — all fields optional):
    {
        "candidate": {
            "first_name": "...",
            "last_name": "...",
            "full_name": "...",
            "email": "..." | ["..."],
            "phone": "..." | ["..."],
            "headline": "...",
            "title": "...",
            "location": "...",
            "city": "...",
            "state": "...",
            "country": "...",
            "skills": ["..."],
            "tags": ["..."],
            "links": ["..."],
            "social_profiles": [{"url": "..."}],
            "experience": [
                {
                    "company": "...",
                    "title": "...",
                    "start_date": "...",
                    "end_date": "...",
                    "description": "..."
                }
            ],
            "education": [
                {
                    "institution": "...",
                    "school": "...",
                    "degree": "...",
                    "field_of_study": "...",
                    "end_year": ...
                }
            ]
        }
    }

    Also supports flat (non-nested) JSON where the
    candidate fields are at the top level.
    """

    ########################################################
    # Load JSON from file or raw string
    ########################################################

    def _load_json(self, source: str) -> dict:

        source = source.strip()

        # Try as file path first
        if not source.startswith("{") and not source.startswith("["):
            try:
                with open(source, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, OSError):
                pass

        # Try as raw JSON string
        return json.loads(source)

    ########################################################
    # Normalize to list
    ########################################################

    def _to_list(self, value) -> list:

        if value is None:
            return []

        if isinstance(value, list):
            return [str(v) for v in value if v]

        return [str(value)] if value else []

    ########################################################
    # Extract name
    ########################################################

    def _extract_name(self, data: dict) -> str:

        if data.get("full_name"):
            return str(data["full_name"])

        first = data.get("first_name", "")
        last = data.get("last_name", "")

        name = f"{first} {last}".strip()

        if name:
            return name

        return data.get("name", None)

    ########################################################
    # Extract location
    ########################################################

    def _extract_location(self, data: dict) -> dict:

        # If location is already structured
        if isinstance(data.get("location"), dict):
            loc = data["location"]
            return {
                "city": loc.get("city"),
                "region": loc.get("region", loc.get("state")),
                "country": loc.get("country"),
            }

        # Build from separate fields
        city = data.get("city", "")
        region = data.get("state", data.get("region", ""))
        country = data.get("country", "")

        # If location is a string, try to parse it
        if isinstance(data.get("location"), str) and data["location"]:
            parts = [p.strip() for p in data["location"].split(",")]
            if len(parts) >= 1 and not city:
                city = parts[0]
            if len(parts) >= 2 and not region:
                region = parts[1]
            if len(parts) >= 3 and not country:
                country = parts[2]

        location = {}
        if city:
            location["city"] = str(city)
        if region:
            location["region"] = str(region)
        if country:
            location["country"] = str(country)

        return location

    ########################################################
    # Extract links
    ########################################################

    def _extract_links(self, data: dict) -> dict:

        raw_links = self._to_list(data.get("links"))

        # Also gather from social_profiles
        for profile in data.get("social_profiles", []):

            if isinstance(profile, dict) and profile.get("url"):

                raw_links.append(str(profile["url"]))

            elif isinstance(profile, str):

                raw_links.append(profile)

        # Deduplicate
        raw_links = list(dict.fromkeys(raw_links))

        # Classify links
        linkedin = None
        github = None
        portfolio = None
        other = []

        for link in raw_links:
            link_lower = link.lower()
            if "linkedin.com" in link_lower:
                linkedin = link
            elif "github.com" in link_lower:
                github = link
            elif any(kw in link_lower for kw in ["portfolio", "personal", ".dev", ".me"]):
                portfolio = link
            else:
                other.append(link)

        return {
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio,
            "other": other,
        }

    ########################################################
    # Extract experience
    ########################################################

    def _normalize_date(self, date_str):
        """Convert various date formats to YYYY-MM."""
        if not date_str:
            return ""
        date_str = str(date_str).strip()
        # Already YYYY-MM
        if len(date_str) == 7 and date_str[4] == "-":
            return date_str
        # YYYY-MM-DD or longer
        if len(date_str) >= 10 and date_str[4] == "-":
            return date_str[:7]
        # Just a year
        if len(date_str) == 4 and date_str.isdigit():
            return f"{date_str}-01"
        return date_str

    def _extract_experience(self, data: dict) -> list:

        raw_exp = data.get("experience", [])

        if not isinstance(raw_exp, list):
            return []

        experience = []

        for entry in raw_exp:

            if not isinstance(entry, dict):
                continue

            start = entry.get(
                "start_date",
                entry.get("start", "")
            )
            end = entry.get(
                "end_date",
                entry.get("end", "")
            )

            experience.append({
                "company": entry.get("company", ""),
                "title": entry.get(
                    "title",
                    entry.get("role", "")
                ),
                "start": self._normalize_date(start),
                "end": self._normalize_date(end),
                "summary": entry.get(
                    "description",
                    entry.get("summary", "")
                ),
            })

        return experience

    ########################################################
    # Extract education
    ########################################################

    def _extract_education(self, data: dict) -> list:

        raw_edu = data.get("education", [])

        if not isinstance(raw_edu, list):
            return []

        education = []

        for entry in raw_edu:

            if not isinstance(entry, dict):
                continue

            institution = entry.get(
                "institution",
                entry.get("school",
                    entry.get("university", ""))
            )

            education.append({
                "institution": institution,
                "degree": entry.get("degree", ""),
                "field": entry.get(
                    "field_of_study",
                    entry.get("field",
                        entry.get("major", ""))
                ),
                "end_year": entry.get("end_year"),
            })

        return education

    ########################################################
    # Extract skills
    ########################################################

    def _extract_skills(self, data: dict) -> list:

        skills = self._to_list(data.get("skills"))

        tags = self._to_list(data.get("tags"))

        return list(dict.fromkeys(skills + tags))

    ########################################################
    # Main parse method
    ########################################################

    def parse(self, source_path: str) -> List[RawCandidate]:

        logger.info(
            "Parsing ATS JSON blob..."
        )

        raw = self._load_json(source_path)

        if isinstance(raw, list):
            items = raw
        elif "candidates" in raw and isinstance(raw["candidates"], list):
            items = raw["candidates"]
        elif "applicants" in raw and isinstance(raw["applicants"], list):
            items = raw["applicants"]
        else:
            items = [raw]

        candidates = []
        for raw_item in items:
            ####################################################
            # Unwrap nested "candidate" key if present
            ####################################################

            if "candidate" in raw_item and isinstance(raw_item["candidate"], dict):
                data = raw_item["candidate"]
            elif "applicant" in raw_item and isinstance(raw_item["applicant"], dict):
                data = raw_item["applicant"]
            else:
                data = raw_item

        ####################################################
        # Extract fields
        ####################################################

            full_name = self._extract_name(data)

            headline = (
                data.get("headline")
                or data.get("title")
                or data.get("current_title")
            )

            emails = self._to_list(
                data.get("email", data.get("emails"))
            )

            phones = self._to_list(
                data.get("phone", data.get("phones"))
            )

            location = self._extract_location(data)
            links = self._extract_links(data)
            skills = self._extract_skills(data)
            experience = self._extract_experience(data)
            education = self._extract_education(data)

            candidates.append(RawCandidate(
                source="ATS JSON",
                full_name=full_name,
                headline=headline,
                location=location,
                emails=emails,
                phones=phones,
                skills=skills,
                experience=experience,
                education=education,
                links=links,
            ))

        logger.info(
            f"ATS JSON parsed: {len(candidates)} candidates"
        )
        return candidates
