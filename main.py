from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recomendations.config.logging_config import configure_logging
from recomendations.core.api.recomendations_router import RecomendationsRestController
from dotenv import load_dotenv
import logging
import os

load_dotenv()
configure_logging()
logger = logging.getLogger("MAIN")

logger.info("Iniciando aplicación FastAPI...")

app = FastAPI(title="Recomendations Microservice")

# =========================
# 🚀 Configuración CORS
# =========================
ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================

logger.info("Registrando rutas...")
app.include_router(RecomendationsRestController.router)  # type: ignore
logger.info("Rutas cargadas correctamente.")


@app.get("/")
async def root():
    logger.info("Root endpoint solicitado.")
    return {"message": "API de Recomendaciones corriendo!"}
