from pydantic import BaseModel, Field
from typing import Optional

class PatientIn(BaseModel):
    name: str
    age: int
    diagnosis: Optional[str] = None

class PatientOut(PatientIn):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
