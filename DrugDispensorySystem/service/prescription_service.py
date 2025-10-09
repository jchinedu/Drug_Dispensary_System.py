from datetime import datetime
from bson import ObjectId
from DrugDispensorySystem.config.db import db
from DrugDispensorySystem.Repository import (
    prescription_repository,
    patient_repository,
    doctor_repository,
)



def serialize_prescription(prescription: dict) -> dict:

    if "_id" in prescription:
        prescription["id"] = str(prescription["_id"])
        del prescription["_id"]


    prescription["code"] = prescription.get("rx_code") or "N/A"


    created_at = prescription.get("created_at") or prescription.get("createdAt")
    if isinstance(created_at, datetime):
        prescription["created_at"] = created_at
    else:
        try:
            prescription["created_at"] = datetime.fromisoformat(str(created_at))
        except Exception:
            prescription["created_at"] = datetime.utcnow()


    prescription["doctor_username"] = prescription.get("doctor_username", "Unknown")
    prescription["patient_name"] = prescription.get("patient_name", "Unknown")
    prescription["status"] = prescription.get("status", "PENDING")

    return prescription


async def create_prescription(prescription_data: dict, doctor_user: dict | None = None) -> str:


    from DrugDispensorySystem.utils.rx_code_generator import generate_rx_code


    prescription_data["rx_code"] = generate_rx_code()
    prescription_data["created_at"] = datetime.utcnow()


    if doctor_user:
        prescription_data["doctor_id"] = doctor_user.get("user_id")
        prescription_data["doctor_username"] = doctor_user.get("username")


    if isinstance(prescription_data.get("patient_id"), ObjectId):
        prescription_data["patient_id"] = str(prescription_data["patient_id"])


    return await prescription_repository.create_prescription(prescription_data)

async def get_prescription_by_id(prescription_id: str) -> dict:
    prescription = await prescription_repository.get_prescription_by_id(prescription_id)
    if not prescription:
        raise ValueError("Prescription not found")


    patient_id = str(prescription.get("patient_id", ""))
    patient = None
    if patient_id and ObjectId.is_valid(patient_id):
        try:
            patient = await patient_repository.get_patient_by_id(patient_id)
        except Exception:
            pass
    prescription["patient_name"] = patient.get("name") if patient else "Unknown"


    doctor_id = (
        prescription.get("doctor_id")
        or prescription.get("created_by_doctor_id")
        or prescription.get("created_by")
    )
    doctor_username = (
        prescription.get("created_by_doctor_username")
        or prescription.get("created_by")
        or prescription.get("doctor_username")
    )

    doctor = None
    if doctor_id and ObjectId.is_valid(str(doctor_id)):
        try:
            doctor = await doctor_repository.get_doctor_by_id(str(doctor_id))
        except Exception:
            pass

    if doctor:
        prescription["doctor_username"] = doctor.get("username") or doctor.get("name", "Unknown")
    else:
        prescription["doctor_username"] = doctor_username or "Unknown"

    return serialize_prescription(prescription)



async def get_prescription_by_code(rx_code: str) -> dict:
    prescription = await db.prescriptions.find_one({"rx_code": rx_code})
    if not prescription:
        return None


    patient_id = str(prescription.get("patient_id", ""))
    patient = None
    if patient_id and ObjectId.is_valid(patient_id):
        try:
            patient = await patient_repository.get_patient_by_id(patient_id)
        except Exception:
            pass
    prescription["patient_name"] = patient.get("name") if patient else "Unknown"


    doctor_id = (
        prescription.get("doctor_id")
        or prescription.get("created_by_doctor_id")
        or prescription.get("created_by")
    )
    doctor_username = (
        prescription.get("created_by_doctor_username")
        or prescription.get("created_by")
        or prescription.get("doctor_username")
    )

    doctor = None
    if doctor_id and ObjectId.is_valid(str(doctor_id)):
        try:
            doctor = await doctor_repository.get_doctor_by_id(str(doctor_id))
        except Exception:
            pass

    if doctor:
        prescription["doctor_username"] = doctor.get("username") or doctor.get("name", "Unknown")
    else:
        prescription["doctor_username"] = doctor_username or "Unknown"

    return serialize_prescription(prescription)



async def get_all_prescriptions():
    prescriptions = await prescription_repository.get_all_prescriptions()
    enriched = []

    for p in prescriptions:

        patient_id = str(p.get("patient_id", ""))
        patient = None
        if patient_id and ObjectId.is_valid(patient_id):
            try:
                patient = await patient_repository.get_patient_by_id(patient_id)
            except Exception:
                pass
        p["patient_name"] = patient.get("name") if patient else "Unknown"


        doctor_id = (
            p.get("doctor_id")
            or p.get("created_by_doctor_id")
            or p.get("created_by")
        )
        doctor_username = (
            p.get("created_by_doctor_username")
            or p.get("created_by")
            or p.get("doctor_username")
        )

        doctor = None
        if doctor_id and ObjectId.is_valid(str(doctor_id)):
            try:
                doctor = await doctor_repository.get_doctor_by_id(str(doctor_id))
            except Exception:
                pass

        if doctor:
            p["doctor_username"] = doctor.get("username") or doctor.get("name", "Unknown")
        else:
            p["doctor_username"] = doctor_username or "Unknown"

        enriched.append(serialize_prescription(p))

    return enriched

async def update_prescription(prescription_id: str, update_data: dict) -> bool:
    success = await prescription_repository.update_prescription(prescription_id, update_data)
    if not success:
        raise ValueError("Failed to update prescription")
    return True


async def delete_prescription(prescription_id: str) -> bool:
    success = await prescription_repository.delete_prescription(prescription_id)
    if not success:
        raise ValueError("Failed to delete prescription")
    return True
