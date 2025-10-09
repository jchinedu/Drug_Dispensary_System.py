import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic_core import core_schema  # ✅ Correct import for Pydantic v2

from DrugDispensorySystem.Model.drugs import DrugModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: Any) -> dict:
        return {"type": "string", "format": "objectid"}


class PrescriptionIn(BaseModel):
    created_by_doctor_username: str
    patient_id: str
    drugs: List[DrugModel]
    status: Optional[str] = "PENDING"
    pharmacist_remarks: Optional[str] = None


class PrescriptionOut(PrescriptionIn):
    code: str
    created_at: datetime.datetime
    dispensed_by_pharmacist: Optional[str] = None
    dispensed_at: Optional[datetime.datetime] = None
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            ObjectId: str,
            datetime.datetime: lambda dt: dt.isoformat()
        }
    }
