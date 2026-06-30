class EmailNormalizer:

    def normalize(self, emails):

        normalized = []

        seen = set()

        for email in emails:

            email = email.strip().lower()

            if email not in seen:

                seen.add(email)

                normalized.append(email)

        return normalized