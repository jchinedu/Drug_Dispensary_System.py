from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    DOCTOR = "doctor"
    PHARMACIST = "pharmacist"

class UserIn(BaseModel):
    username: str
    full_name: str
    role: UserRole
    password: str

class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    full_name: str
    role: UserRole

    class Config:
        allow_population_by_field_name = True
