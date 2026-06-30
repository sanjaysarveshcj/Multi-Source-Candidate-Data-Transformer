import re


class ContactExtractor:

    EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE_REGEX = (
        r"(?:\+?\d{1,3}[-.\s]?)?"
        r"(?:\(?\d{3}\)?[-.\s]?)?"
        r"\d{3}[-.\s]?\d{4}"
    )

    LINK_REGEX = r"https?://[^\s]+"

    LINKEDIN_REGEX = r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s]+"

    GITHUB_REGEX = r"(?:https?://)?(?:www\.)?github\.com/[^\s]+"

    def extract(self, text: str):

        emails = list(set(re.findall(self.EMAIL_REGEX, text)))

        phones = list(set(re.findall(self.PHONE_REGEX, text)))

        links = list(set(re.findall(self.LINK_REGEX, text)))

        linkedin = list(set(re.findall(self.LINKEDIN_REGEX, text)))

        github = list(set(re.findall(self.GITHUB_REGEX, text)))

        return {
            "emails": emails,
            "phones": phones,
            "links": links,
            "linkedin": linkedin,
            "github": github,
        }