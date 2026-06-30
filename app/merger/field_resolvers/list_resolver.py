class ListResolver:

    def resolve(self, candidates, field):

        merged = []

        seen = set()

        sources = []

        for candidate in candidates:

            values = getattr(candidate, field)

            for value in values:

                if value not in seen:

                    seen.add(value)

                    merged.append(value)

                    sources.append(candidate.source)

        return merged, sources