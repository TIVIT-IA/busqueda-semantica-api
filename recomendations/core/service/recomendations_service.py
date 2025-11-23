from abc import ABC, abstractmethod
from recomendations.schema.recomendation_schema import RequirementRequest, RequirementResponse


class RecomendationsService(ABC):

    @abstractmethod
    def recommend(self, t: RequirementRequest) -> RequirementResponse:
        pass


