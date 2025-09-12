import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from DrugDispensorySystem.Model.drugs import DrugModel


class PrescriptionIn(BaseModel):
    created_by_doctor_username: str
    patient_id: str
    drugs: List[DrugModel]
    status: Optional[str] = "PENDING"
    pharmacist_remarks: Optional[str] = None

class PrescriptionOut(PrescriptionIn):
    code: str
    created_at: datetime
    dispensed_by_pharmacist: Optional[str] = None
    dispensed_at: Optional[datetime] = None
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
