from typing import Optional, List, Any
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic_core import core_schema
import logging
import traceback

from starlette import status

from DrugDispensorySystem.Repository import patient_repository
from DrugDispensorySystem.service import patient_service, prescription_service
from DrugDispensorySystem.service.auth_service import get_current_user
from DrugDispensorySystem.service.patient_service import serialize_patient

router = APIRouter(prefix="/doctor", tags=["Doctor"])


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


class PatientCreate(BaseModel):
    name: str
    age: int
    diagnosis: str

class PatientResponse(BaseModel):
    id: str
    name: str
    age: int
    diagnosis: str

class DrugDetail(BaseModel):
    name: str
    quantity: int
    drug_type: str
    days_to_use: int

class PrescriptionCreate(BaseModel):
    patient_id: str
    drugs: List[DrugDetail]
    notes: Optional[str] = None

class PrescriptionOut(BaseModel):
    id: PyObjectId = Field(alias="_id")
    patient_id: str
    doctor_id: str
    drugs: List[DrugDetail]
    notes: Optional[str] = None
    status: Optional[str] = "PENDING"
    created_at: datetime
    rx_code: str

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
    }


@router.get("/patients", response_model=List[PatientResponse])
async def get_all_patients(current_user: dict = Depends(get_current_user)):

    if current_user.get("role") != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        doctor_id = current_user["user_id"]
        patients = await patient_service.get_all_patients_by_doctor(doctor_id)
        serialized_patients = [serialize_patient(p) for p in patients if "_id" in p]
        return serialized_patients
    except Exception:
        logging.error("Error fetching patients:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error fetching patients")


@router.post("/patients", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate, current_user: dict = Depends(get_current_user)):

    if current_user.get("role") != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        patient_data = patient.dict()
        patient_data["doctor_id"] = current_user["user_id"]

        created_patient = await patient_service.create_patient(
            patient_data, doctor_id=current_user["user_id"]
        )
        return created_patient
    except Exception:
        logging.error(" Error creating patient:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error creating patient")


@router.post("/prescriptions")
async def create_prescription(
    prescription: PrescriptionCreate,
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        prescription_dict = prescription.dict()
        prescription_dict["doctor_id"] = current_user["user_id"]
        prescription_dict["doctor_username"] = current_user["username"]
        prescription_dict["created_at"] = datetime.utcnow()


        from DrugDispensorySystem.utils.rx_code_generator import generate_rx_code
        prescription_dict["rx_code"] = generate_rx_code()


        prescription_id = await prescription_service.create_prescription(prescription_dict)

        return {
            "success": True,
            "message": "Prescription created successfully",
            "prescription_id": str(prescription_id)
        }
    except Exception as e:
        import traceback, logging
        logging.error(" Error creating prescription:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error creating prescription")


@router.get("/prescriptions")
async def get_all_prescriptions(current_user: dict = Depends(get_current_user)):

    if current_user.get("role") != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")

    try:

        prescriptions = await prescription_service.get_all_prescriptions()


        for pres in prescriptions:
            patient = await patient_repository.get_patient_by_id(pres.get("patient_id"))
            pres["patient_name"] = patient["name"] if patient else "Unknown patient"

        return prescriptions

    except Exception as e:
        import traceback, logging
        logging.error(" Error fetching prescriptions:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error fetching prescriptions")
