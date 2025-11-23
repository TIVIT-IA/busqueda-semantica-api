from recomendations.config.tei_client import TEIClient
from recomendations.core.service.recomendations_service import RecomendationsService
from recomendations.core.repository.professional_repository import ProfessionalRepository
from recomendations.schema.recomendation_schema import RequirementRequest


class RecomendationsServiceImpl(RecomendationsService):

    def __init__(self):
        self.embeddings = TEIClient("http://localhost:8090")
        self.repo = ProfessionalRepository()

    async def recommend(self, t: RequirementRequest) -> dict:
        if not t.requirement.strip():
            return {"error": "El campo 'requirement' está vacío"}

        try:
            vector = await self.embeddings.embed(t.requirement)
            if isinstance(vector, list) and len(vector) > 0 and isinstance(vector[0], list):
                vector = vector[0]
        except Exception as e:
            return {"error": f"Error llamando al servicio TEI: {e}"}

        rows = self.repo.search_by_vector(vector, t.limit)
        filtered = [r for r in rows if r.get("distancia", 999) <= t.umbral]

        return self._build_response(filtered)



    def _build_response(self, rows: list[dict]) -> dict:
        response = {"results": []}

        for r in rows:
            item = {
                "distancia": r.get("distancia"),
                "match_score": round((2 - r["distancia"]), 4),
            }

            for key, val in r.items():
                if key not in item:
                    item[key] = val

            response["results"].append(item)

        return response