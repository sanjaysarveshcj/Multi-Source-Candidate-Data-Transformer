from app.models.metadata import Provenance


class ProvenanceBuilder:

    def build(self, field, source, confidence):

        return Provenance(
            field=field,
            source=source,
            method="merge",
            confidence=confidence
        )