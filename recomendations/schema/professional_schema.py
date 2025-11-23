from pydantic import BaseModel
from typing import List

class SkillResponse(BaseModel):
    name: str | None = None

class ProfessionalResponse(BaseModel):
    name: str | None = None
    role: str | None = None
    match_level: str | None = None
    experience: str | None = None
    skills: List[SkillResponse] | None = None
