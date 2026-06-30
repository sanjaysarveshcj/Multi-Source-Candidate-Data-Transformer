class NameExtractor:
    """
    Extracts candidate name from the resume header.
    Assumption:
        First non-empty line of the resume is the candidate's name.
    """

    def extract(self, header: str):

        lines = [
            line.strip()
            for line in header.split("\n")
            if line.strip()
        ]

        if not lines:
            return None

        return lines[0]