from app.models.candidate import Candidate

from app.merger.field_registry import FIELD_CONFIG

from app.provenance.provenance_builder import ProvenanceBuilder

from app.confidence.confidence_engine import ConfidenceEngine

from app.utils.id_generator import CandidateIdGenerator


class MergeEngine:

    def __init__(self):

        self.provenance_builder = ProvenanceBuilder()

        self.confidence_engine = ConfidenceEngine()

        self.id_generator = CandidateIdGenerator()

    def merge(self, candidates):

        candidate = Candidate()

        provenance = []

        ############################################
        # Iterate over every registered field
        ############################################

        for field, config in FIELD_CONFIG.items():

            resolver = config["resolver"]

            normalizer = config["normalizer"]

            value, sources = resolver.resolve(
                candidates,
                field
            )

            if normalizer is not None:

                value = normalizer.normalize(value)

            setattr(candidate, field, value)

            ##########################################
            # Provenance
            ##########################################

            for source in set(sources):

                provenance.append(

                    self.provenance_builder.build(

                        field,

                        source,

                        self.confidence_engine.score(source)

                    )

                )

        ############################################
        # Overall Confidence
        ############################################

        scores = [

            self.confidence_engine.score(c.source)

            for c in candidates

        ]

        if scores:

            candidate.overall_confidence = (

                sum(scores) / len(scores)

            )

        ############################################
        # Candidate ID
        ############################################

        candidate.candidate_id = (

            self.id_generator.generate(candidate)

        )

        ############################################
        # Provenance
        ############################################

        candidate.provenance = provenance

        return candidate