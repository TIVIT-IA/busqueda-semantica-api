import logging
from recomendations.config.tei_client import TEIClient
from recomendations.core.service.recomendations_service import RecomendationsService
from recomendations.core.repository.professional_repository import ProfessionalRepository


class RecomendationsServiceImpl(RecomendationsService):

    def __init__(self):
        self.logger = logging.getLogger("RecomendationsService")
        self.logger.info("Inicializando servicio...")
        
        self.embeddings = TEIClient("http://localhost:8090")
        self.repo = ProfessionalRepository()

        self.logger.info("Servicio inicializado correctamente.")

    async def recommend(self, t: dict) -> dict:
        self.logger.info("Nueva solicitud de recomendación.")
        self.logger.debug(f"Payload recibido: {t}")

        # 1. Extraer requirement
        requirement_text = (
            t.get("requirement")
            or t.get("texto")
            or t.get("input")
        )

        if not requirement_text:
            self.logger.error("No se encontró campo requirement en el JSON.")
            return {"error": "El JSON no contiene un campo válido de requirement"}

        self.logger.info("Requirement extraído.")
        self.logger.debug(f"Requirement: {requirement_text}")

        # 2. Obtener embedding
        try:
            self.logger.info("Solicitando embedding al servicio TEI...")
            vector = await self.embeddings.embed(requirement_text)
            self.logger.info("Embedding recibido.")

            # Normalizar si viene [[...]]
            if isinstance(vector[0], list):
                self.logger.debug("Normalizando embedding anidado.")
                vector = vector[0]

            self.logger.debug(f"Dimensión embedding: {len(vector)}")

        except Exception as e:
            self.logger.error(f"ERROR obteniendo embedding: {e}")
            return {"error": f"Error llamando al servicio TEI: {e}"}

        # 3. Buscar en la BD
        LIMIT = t.get("limit", 10)
        self.logger.info(f"Buscando similitudes en la BD. LIMIT={LIMIT}")

        rows = self.repo.search_by_vector(vector, LIMIT)
        self.logger.info(f"{len(rows)} registros encontrados.")

        # 4. Filtrado dinámico
        umbral = t.get("threshold", 2.0)
        self.logger.info(f"Aplicando threshold: {umbral}")

        filtered = [r for r in rows if r.get("distancia", 999) <= umbral]
        self.logger.info(f"{len(filtered)} registros luego del filtrado.")

        # 5. Construir response
        response = {"results": []}
        self.logger.info("Construyendo respuesta final...")

        for r in filtered:
            item = {
                "distancia": r.get("distancia"),
                "match_score": round((2 - r["distancia"]), 4),
            }

            for key, val in r.items():
                if key not in item:
                    item[key] = val

            response["results"].append(item)

        self.logger.info("Respuesta generada correctamente.")
        return response
