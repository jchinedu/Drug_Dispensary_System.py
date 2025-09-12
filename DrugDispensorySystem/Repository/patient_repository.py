from DrugDispensorySystem.config.db import db

patients_collection = db["patients"]

async def create_patient(patient_data: dict):
    result = await patients_collection.insert_one(patient_data)
    return str(result.inserted_id)

async def get_patient_by_id(patient_id: str):
    from bson import ObjectId
    return await patients_collection.find_one({"_id": ObjectId(patient_id)})

async def get_all_patients():
    cursor = patients_collection.find({})
    return await cursor.to_list(length=100)

async def update_patient(patient_id: str, update_data: dict):
    from bson import ObjectId
    result = await patients_collection.update_one(
        {"_id": ObjectId(patient_id)}, {"$set": update_data}
    )
    return result.modified_count > 0
