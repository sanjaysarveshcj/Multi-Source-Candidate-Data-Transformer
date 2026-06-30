from abc import ABC, abstractmethod


class BaseResolver(ABC):

    @abstractmethod
    def resolve(self, candidates, field):
        pass