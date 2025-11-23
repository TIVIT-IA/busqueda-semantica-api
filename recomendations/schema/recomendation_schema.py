from pydantic import BaseModel
from typing import List
from recomendations.schema.professional_schema import ProfessionalResponse


class RequirementRequest(BaseModel):
    requirement: str 
    limit: int = 10        
    umbral: float = 2.0  


class RequirementResponse(BaseModel):
    professionals: List[ProfessionalResponse] | None = None
