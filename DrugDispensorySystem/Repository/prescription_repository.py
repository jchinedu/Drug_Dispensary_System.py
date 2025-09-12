from DrugDispensorySystem.config.db import db

prescriptions_collection = db["prescriptions"]

async def create_prescription(prescription_data: dict):
    result = await prescriptions_collection.insert_one(prescription_data)
    return str(result.inserted_id)

async def get_prescription_by_id(prescription_id: str):
    from bson import ObjectId
    return await prescriptions_collection.find_one({"_id": ObjectId(prescription_id)})

async def get_prescriptions_by_patient(patient_id: str):
    return await prescriptions_collection.find({"patient_id": patient_id}).to_list(100)

async def update_prescription(prescription_id: str, update_data: dict):
    from bson import ObjectId
    result = await prescriptions_collection.update_one(
        {"_id": ObjectId(prescription_id)}, {"$set": update_data}
    )
    return result.modified_count > 0
