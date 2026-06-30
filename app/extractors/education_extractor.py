import re

from app.logging.logger import logger


class EducationExtractor:

    DEGREE_PATTERN = re.compile(
        r"(Bachelor(?:'s)?|Master(?:'s)?|B\.?\s?E\.?|B\.?\s?Tech|M\.?\s?Tech|"
        r"BCA|MCA|BSc|MSc|MBA|PhD|Diploma|Associate)",
        re.IGNORECASE,
    )

    DATE_PATTERN = re.compile(
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
        r"[a-z]*\s+\d{4})",
        re.IGNORECASE,
    )

    CGPA_PATTERN = re.compile(
        r"(CGPA|GPA|Percentage)\s*:?\s*([\d.]+(?:/\d+(?:\.\d+)?)?)",
        re.IGNORECASE,
    )

    LOCATION_PATTERN = re.compile(
        r"[A-Za-z .]+,\s*[A-Z]{2,}"
    )

    INSTITUTION_KEYWORDS = [
        "University",
        "Institute",
        "College",
        "School",
        "Academy",
        "Polytechnic"
    ]

    def extract(self, sections):

        logger.info("Extracting education information...")

        education_lines = sections.get("education", [])

        if not education_lines:
            logger.info("No education section found")
            return []

        blocks = self._group_blocks(education_lines)

        logger.info(
            f"Education blocks identified: {len(blocks)}"
        )

        result = []

        for block in blocks:
            result.append(self._parse_block(block))

        logger.info(
            f"Education extraction complete: {len(result)} entries"
        )

        return result

    ####################################################

    def _group_blocks(self, lines):

        blocks = []
        current = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if self._is_new_record(line) and current:
                has_inst = any(self._is_new_record(c) for c in current)
                if has_inst:
                    blocks.append(current)
                    current = []

            current.append(line)

        if current:
            blocks.append(current)

        return blocks

    ####################################################

    def _is_new_record(self, line):

        if "|" in line:
            return True

        for keyword in self.INSTITUTION_KEYWORDS:
            if keyword.lower() in line.lower():
                return True

        return False

    ####################################################

    def _parse_block(self, block):

        text = " ".join(block)

        return {

            "institution": self._extract_institution(block),

            "degree": self._extract_degree(text),

            "location": self._extract_location(text),

            "start_date": self._extract_dates(text)[0],

            "end_date": self._extract_dates(text)[1],

            "cgpa": self._extract_cgpa(text),

            "field_of_study": self._extract_field_of_study(text),

            "raw": block
        }

    ####################################################

    def _extract_institution(self, block):

        for line in block:
            if "|" in line:
                return line.split("|")[0].strip()
            
            for keyword in self.INSTITUTION_KEYWORDS:
                if keyword.lower() in line.lower():
                    # If the line contains an institution keyword, it's likely the institution name
                    # We can remove dates if they exist on the same line, but typically it's just the name
                    # For safety, let's just return the line (or split by comma if needed, but returning line is safe)
                    return line.split(",")[0].strip()

        # Fallback to the first line
        return block[0]

    ####################################################

    def _extract_degree(self, text):

        match = self.DEGREE_PATTERN.search(text)

        if match:
            return match.group(0)

        return None

    ####################################################

    def _extract_location(self, text):

        match = self.LOCATION_PATTERN.search(text)

        if match:
            return match.group(0)

        return None

    ####################################################

    def _extract_dates(self, text):

        matches = self.DATE_PATTERN.findall(text)

        if len(matches) >= 2:
            return matches[0], matches[1]

        if len(matches) == 1:
            return matches[0], None

        return None, None

    ####################################################

    def _extract_cgpa(self, text):

        match = self.CGPA_PATTERN.search(text)

        if match:
            return match.group(2)

        return None

    ####################################################

    def _extract_field_of_study(self, text):

        degree = self._extract_degree(text)

        if not degree:
            return None

        idx = text.lower().find(degree.lower())

        if idx == -1:
            return None

        remaining = text[idx + len(degree):]

        remaining = remaining.replace("(", "")
        remaining = remaining.replace(")", "")

        stop_words = [
            "CGPA",
            "GPA",
            "Percentage",
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Sept",
            "Oct",
            "Nov",
            "Dec"
        ]

        for word in stop_words:

            pos = remaining.lower().find(word.lower())

            if pos != -1:
                remaining = remaining[:pos]

        remaining = remaining.strip(" -|,")

        return remaining if remaining else None