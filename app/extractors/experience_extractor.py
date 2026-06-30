import re

from app.logging.logger import logger


class ExperienceExtractor:

    EXPERIENCE_HEADER = re.compile(
        r"(experience|work experience|employment|professional experience)",
        re.I,
    )

    MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"

    COMPANY_PATTERN = re.compile(
        rf"^(.*?)\s*\|\s*(.*?)\s*{MONTHS}",
        re.I,
    )

    DATE_PATTERN = re.compile(
        rf"{MONTHS}\s+\d{{4}}\s*-\s*(Present|{MONTHS}\s+\d{{4}})",
        re.I,
    )

    def extract(self, sections):

        logger.info("Extracting experience information...")

        experience = []

        lines = sections.get("experience", [])

        current = None

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # --------------------------------------------------
            # New Company Entry
            # --------------------------------------------------

            if "|" in line and self.DATE_PATTERN.search(line):

                if current:
                    experience.append(current)

                current = self.parse_job(line)

            elif line.startswith("•") or line.startswith("-"):

                if current:
                    current["description"].append(
                        line.lstrip("•- ").strip()
                    )

            else:

                if current:
                    current["description"].append(line)

        if current:
            experience.append(current)

        logger.info(
            f"Experience extraction complete: {len(experience)} entries"
        )

        return experience

    # --------------------------------------------------

    def parse_job(self, line):

        company = ""

        title = ""

        employment_type = None

        start = None

        end = None

        parts = line.split("|")

        if len(parts) >= 2:

            company = parts[0].strip()

            remaining = parts[1].strip()

        else:

            remaining = line

        date_match = self.DATE_PATTERN.search(line)

        if date_match:

            dates = date_match.group()

            start, end = [
                x.strip()
                for x in dates.split("-")
            ]

            remaining = remaining.replace(
                dates,
                ""
            ).strip()

        emp_match = re.search(
            r"\((.*?)\)",
            remaining
        )

        if emp_match:

            employment_type = emp_match.group(1)

            remaining = re.sub(
                r"\(.*?\)",
                "",
                remaining,
            ).strip()

        title = remaining

        return {
            "company": company,
            "title": title,
            "employment_type": employment_type,
            "start_date": start,
            "end_date": end,
            "description": [],
        }