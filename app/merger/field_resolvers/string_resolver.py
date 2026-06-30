from app.settings import SOURCE_PRIORITY


class StringResolver:

    def resolve(self, candidates, field):

        ordered = sorted(
            candidates,
            key=lambda c: SOURCE_PRIORITY.get(c.source, 999)
        )

        for candidate in ordered:

            value = getattr(candidate, field)

            if value:

                return value, [candidate.source]

        return None, []