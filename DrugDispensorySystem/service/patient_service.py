from typing import Dict, Any, List
from fastapi import HTTPException
from bson import ObjectId

from DrugDispensorySystem.Repository import patient_repository


def serialize_patient(patient: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name", ""),
        "age": patient.get("age", 0),
        "diagnosis": patient.get("diagnosis", "")
    }

async def create_patient(patient_data: Dict[str, Any], doctor_id: str) -> Dict[str, Any]:
    try:
        patient_data["doctor_id"] = doctor_id
        inserted_id = await patient_repository.create_patient(patient_data)

        if not inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create patient")
        patient = await patient_repository.get_patient_by_id(inserted_id)

        if not patient:
            raise HTTPException(status_code=500, detail="Patient created but not found")
        return serialize_patient(patient)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating patient")



async def get_patient_by_id(patient_id: str) -> Dict[str, Any]:
    try:
        patient = await patient_repository.get_patient_by_id(patient_id)

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        return serialize_patient(patient)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching patient")


async def get_all_patients(doctor_id: str) -> List[Dict[str, Any]]:

    try:
        patients = await patient_repository.get_all_patients_by_doctor(doctor_id)

        serialized = [serialize_patient(p) for p in patients if "_id" in p]
        return serialized
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching patients")



async def get_all_patients_by_doctor(doctor_id: str):

    try:
        patients = await patient_repository.get_all_patients_by_doctor(str(doctor_id))
        return patients
    except Exception as e:
        print(f" Error in patient_service.get_all_patients_by_doctor: {e}")
        return []



async def update_patient(patient_id: str, update_data: Dict[str, Any]) -> bool:

    try:
        success = await patient_repository.update_patient(patient_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Failed to update patient")

        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating patient")


async def delete_patient(patient_id: str) -> bool:

    try:
        success = await patient_repository.delete_patient(patient_id)

        if not success:
            raise HTTPException(status_code=404, detail="Failed to delete patient")

        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting patient")
