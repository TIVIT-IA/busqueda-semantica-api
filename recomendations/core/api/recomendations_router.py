import logging
from recomendations.config.routers_config import BaseController, post, router
from recomendations.core.service.recomendations_service import RecomendationsService
from recomendations.config.dependency_injection import inject
from fastapi import Body

logger = logging.getLogger("Router")

@router("/recomendations")
@inject("service", RecomendationsService)
class RecomendationsRestController(BaseController):

    @post("/recommend")
    async def recommend(self, payload: dict = Body(...)) -> dict:
        logger.info("POST /recomendations/recommend llamado")
        logger.debug(f"Payload: {payload}")
        return await self.service.recommend(payload)  # type: ignore # AWAIT requerido
