from pydantic import BaseModel

from DrugDispensorySystem.Model.Domain.enums import DrugType


class DrugModel(BaseModel):
    id: str
    name: str
    quantity: int
    drug_type: DrugType
    days_to_use: int
