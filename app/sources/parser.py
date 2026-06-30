from abc import ABC, abstractmethod

from app.models.raw_candidate import RawCandidate


class SourceParser(ABC):

    @abstractmethod
    def parse(self, source_path: str) -> RawCandidate:
        pass