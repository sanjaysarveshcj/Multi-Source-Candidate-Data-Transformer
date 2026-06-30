import hashlib


class CandidateIdGenerator:

    def generate(self, candidate):

        base = ""

        if candidate.full_name:
            base += candidate.full_name

        if candidate.emails:
            base += candidate.emails[0]

        if candidate.phones:
            base += candidate.phones[0]

        return hashlib.md5(base.encode()).hexdigest()