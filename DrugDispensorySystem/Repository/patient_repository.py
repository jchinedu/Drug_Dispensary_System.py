from bson import ObjectId
from typing import Optional, List, Dict, Any

from DrugDispensorySystem.config.db import db

patients_collection = db["patients"]


async def create_patient(patient_data: Dict[str, Any]) -> str:

    try:
        result = await patients_collection.insert_one(patient_data)
        return str(result.inserted_id)
    except Exception as e:
        print(f" Error creating patient: {e}")
        raise


async def get_patient_by_id(patient_id: str) -> Optional[Dict]:

    try:
        return await patients_collection.find_one({"_id": ObjectId(patient_id)})
    except Exception as e:
        print(f" Error fetching patient by ID: {e}")
        return None


async def get_all_patients_by_doctor(doctor_id: str) -> List[Dict]:

    try:
        doctor_id = str(doctor_id)
        cursor = patients_collection.find({"doctor_id": doctor_id})
        patients = await cursor.to_list(length=100)
        print(f"Fetching patients for doctor_id={doctor_id}")
        print("Raw patients from DB:", patients)
        return patients
    except Exception as e:
        print(f"Error fetching patients by doctor: {e}")
        return []

async def get_all_patients() -> List[Dict]:

    try:
        cursor = patients_collection.find({})
        patients = await cursor.to_list(length=100)
        print("Raw patients from DB:", patients)
        return patients
    except Exception as e:
        print(f"Error fetching all patients: {e}")
        return []


async def update_patient(patient_id: str, update_data: Dict[str, Any]) -> bool:

    try:
        result = await patients_collection.update_one(
            {"_id": ObjectId(patient_id)}, {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating patient: {e}")
        return False


async def delete_patient(patient_id: str) -> bool:

    try:
        result = await patients_collection.delete_one({"_id": ObjectId(patient_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f" Error deleting patient: {e}")
        return False
