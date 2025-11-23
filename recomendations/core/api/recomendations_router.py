import logging
from recomendations.config.routers_config import BaseController, post, router
from recomendations.core.service.recomendations_service import RecomendationsService
from recomendations.config.dependency_injection import inject
from recomendations.schema.recomendation_schema import RequirementRequest


@router("/recomendations")
@inject("service", RecomendationsService)
class RecomendationsRestController(BaseController):

    @post("/recommend")
    async def recommend(self, payload: RequirementRequest) -> dict:
        return await self.service.recommend(payload)  # type: ignore
