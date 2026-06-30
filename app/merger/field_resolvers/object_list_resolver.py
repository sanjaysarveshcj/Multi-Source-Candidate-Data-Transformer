class ObjectListResolver:

    def resolve(self, candidates, field):

        merged = []

        seen = set()

        sources = []

        for candidate in candidates:

            values = getattr(candidate, field)

            for obj in values:

                key = str(obj)

                if key not in seen:

                    seen.add(key)

                    merged.append(obj)

                    sources.append(candidate.source)

        return merged, sources