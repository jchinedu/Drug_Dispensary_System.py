from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from DrugDispensorySystem.service import prescription_service

router = APIRouter(prefix="/pharmacist", tags=["Pharmacist"])

class PrescriptionUpdate(BaseModel):
    notes: str
    dispensed: bool = True

@router.get("/prescriptions/{prescription_id}")
async def get_prescription(prescription_id: str):
    try:
        return await prescription_service.get_prescription_by_id(prescription_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Prescription not found")

@router.put("/prescriptions/{prescription_id}")
async def update_prescription(prescription_id: str, data: PrescriptionUpdate):
    update_data = data.dict(exclude_unset=True)
    try:
        await prescription_service.update_prescription(prescription_id, update_data)
        return {"message": "Prescription updated"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Update failed")
