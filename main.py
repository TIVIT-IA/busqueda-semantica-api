from fastapi import FastAPI
from recomendations.config.logging_config import configure_logging
from recomendations.core.api.recomendations_router import RecomendationsRestController
from dotenv import load_dotenv
import logging

load_dotenv()
configure_logging()
logger = logging.getLogger("MAIN")

logger.info("Iniciando aplicación FastAPI...")

app = FastAPI(title="Recomendations Microservice")

logger.info("Registrando rutas...")
app.include_router(RecomendationsRestController.router)  # type: ignore
logger.info("Rutas cargadas correctamente.")

@app.get("/")
async def root():
    logger.info("Root endpoint solicitado.")
    return {"message": "API de Recomendaciones corriendo!"}
