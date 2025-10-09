from enum import Enum
from pydantic import BaseModel, Field, validator

class UserRole(str, Enum):
    DOCTOR = "doctor"
    PHARMACIST = "pharmacist"

class UserIn(BaseModel):
    name: str
    username: str
    email: str
    password: str
    confirm_password: str
    role: UserRole

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str = Field(..., alias="_name")
    username: str
    email: str
    password: str
    role: UserRole

    class Config:
        allow_population_by_field_name = True