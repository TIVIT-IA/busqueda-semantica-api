from pydantic import BaseModel
from typing import List
from recomendations.schema.professional_schema import ProfessionalResponse


class RequirementRequest(BaseModel):
    requirement: str 


class RequirementResponse(BaseModel):
    professionals: List[ProfessionalResponse] | None = None
