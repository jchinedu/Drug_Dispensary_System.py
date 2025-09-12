from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel

from DrugDispensorySystem.service import prescription_service, patient_service

router = APIRouter(prefix="/doctor", tags=["Doctor"])

class PrescriptionCreate(BaseModel):
    patient_id: str
    doctor_id: str
    drugs: List[str]
    notes: Optional[str] = None

@router.get("/patients")
async def get_all_patients():
    return await patient_service.get_all_patients()

@router.post("/prescriptions")
async def create_prescription(prescription: PrescriptionCreate):
    prescription_id = await prescription_service.create_prescription(prescription.dict())
    return {"prescription_id": prescription_id}

@router.get("/prescriptions/by-patient/{patient_id}")
async def get_prescriptions_by_patient(patient_id: str):
    return await prescription_service.get_prescriptions_by_patient(patient_id)
