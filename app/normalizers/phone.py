import re

class PhoneNormalizer:

    def normalize(self, phones):

        result = []

        seen = set()

        for phone in phones:

            digits = re.sub(r"\D", "", phone)

            if len(digits) > 10:
                digits = digits[-10:]

            if digits not in seen:

                seen.add(digits)

                result.append(digits)

        return result