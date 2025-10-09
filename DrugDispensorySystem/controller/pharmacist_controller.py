from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from DrugDispensorySystem.service import prescription_service
from DrugDispensorySystem.Repository import doctor_repository, patient_repository


router = APIRouter(prefix="/pharmacist", tags=["Pharmacist"])


class PrescriptionUpdate(BaseModel):
    pharmacist_username: str
    remarks: str | None = None




@router.get("/prescriptions")
async def get_all_prescriptions():

    try:
        prescriptions = await prescription_service.get_all_prescriptions()
        if not prescriptions:
            raise HTTPException(status_code=404, detail="No prescriptions found")

        enriched = []
        for pres in prescriptions:
            # 🔹 Doctor info
            doctor = None
            doctor_id = pres.get("doctor_id")
            if doctor_id:
                doctor = await doctor_repository.get_doctor_by_id(doctor_id)

            pres["doctor_username"] = (
                doctor.get("username")
                if doctor and "username" in doctor
                else pres.get("created_by_doctor_username", "Unknown")
            )


            patient = None
            patient_id = pres.get("patient_id")
            if patient_id:
                patient = await patient_repository.get_patient_by_id(patient_id)

            pres["patient_name"] = (
                patient.get("name") if patient and "name" in patient else "Unknown"
            )


            pres["code"] = pres.get("rx_code", "N/A")
            pres["status"] = pres.get("status", "PENDING")

            created_at = pres.get("created_at") or pres.get("createdAt")
            if isinstance(created_at, datetime):
                pres["created_at"] = created_at
            else:
                try:
                    pres["created_at"] = datetime.fromisoformat(str(created_at))
                except Exception:
                    pres["created_at"] = datetime.utcnow()

            enriched.append(pres)

        return enriched

    except Exception as e:
        print(f"❌ Error fetching prescriptions: {e}")
        raise HTTPException(status_code=500, detail="Error fetching prescriptions")


@router.get("/prescriptions/{prescription_id}")
async def get_prescription(prescription_id: str):
    try:
        prescription = await prescription_service.get_prescription_by_id(prescription_id)
        if not prescription:
            raise HTTPException(status_code=404, detail="Prescription not found")
        return prescription
    except Exception as e:
        print(f" Error fetching prescription by ID: {e}")
        raise HTTPException(status_code=500, detail="Error fetching prescription")


@router.get("/prescriptions/code/{rx_code}")
async def get_prescription_by_code(rx_code: str):

    try:
        prescription = await prescription_service.get_prescription_by_code(rx_code)
        if not prescription:
            raise HTTPException(status_code=404, detail="Prescription not found")
        if not prescription.get("doctor_username") or prescription["doctor_username"] == "Unknown":
            from DrugDispensorySystem.Repository.doctor_repository import get_doctor_by_id
            doc_id = (
                prescription.get("doctor_id")
                or prescription.get("created_by_doctor_id")
                or prescription.get("created_by")
            )
            if doc_id and ObjectId.is_valid(str(doc_id)):
                doctor = await get_doctor_by_id(str(doc_id))
                if doctor:
                    prescription["doctor_username"] = doctor.get("username") or doctor.get("name", "Unknown")
        from DrugDispensorySystem.Repository.patient_repository import get_patient_by_id
        patient = await get_patient_by_id(prescription.get("patient_id"))
        prescription["patient"] = {
            "name": patient.get("name") if patient else "N/A",
            "age": patient.get("age") if patient else "N/A",
            "diagnosis": patient.get("diagnosis") if patient else "N/A",
        }

        return prescription

    except Exception as e:
        print(f"Error fetching prescription by RX code: {e}")
        raise HTTPException(status_code=500, detail="Error fetching prescription by code")


@router.put("/prescriptions/{prescription_id}/dispense")
async def dispense_prescription(prescription_id: str, data: PrescriptionUpdate):

    try:
        update_data = {
            "status": "DISPENSED",
            "dispensed": True,
            "pharmacist_remarks": data.remarks,
            "dispensed_by_pharmacist": data.pharmacist_username,
            "dispensed_at": datetime.utcnow(),
        }

        success = await prescription_service.update_prescription(prescription_id, update_data)

        if not success:
            raise HTTPException(status_code=400, detail="Failed to update prescription")

        return {"message": "Prescription dispensed successfully"}

    except Exception as e:
        print(f"Error updating prescription: {e}")
        raise HTTPException(status_code=500, detail="Error updating prescription")
