from datetime import datetime
from bson import ObjectId
from DrugDispensorySystem.config.db import db

prescriptions_collection = db["prescriptions"]

async def create_prescription(prescription_data: dict):
    prescription_data["createdAt"] = datetime.utcnow()
    result = await prescriptions_collection.insert_one(prescription_data)
    return str(result.inserted_id)


async def get_prescription_by_id(prescription_id: str):
    if ObjectId.is_valid(prescription_id):
        query = {"_id": ObjectId(prescription_id)}
    else:
        query = {"rx_code": prescription_id}

    prescription = await prescriptions_collection.find_one(query)
    if prescription and "_id" in prescription:
        prescription["_id"] = str(prescription["_id"])
    return prescription


async def get_prescriptions_by_patient(patient_id: str):
    cursor = prescriptions_collection.find({"patient_id": patient_id})
    prescriptions = await cursor.to_list(length=100)
    for p in prescriptions:
        if "_id" in p:
            p["_id"] = str(p["_id"])
    return prescriptions


async def get_all_prescriptions():
    cursor = prescriptions_collection.find({})
    prescriptions = await cursor.to_list(length=1000)
    for p in prescriptions:
        if "_id" in p:
            p["_id"] = str(p["_id"])
    return prescriptions


async def update_prescription(prescription_id: str, update_data: dict):
    query = (
        {"_id": ObjectId(prescription_id)}
        if ObjectId.is_valid(prescription_id)
        else {"rx_code": prescription_id}
    )
    result = await prescriptions_collection.update_one(query, {"$set": update_data})
    return result.modified_count > 0

async def delete_prescription(prescription_id: str):
    query = (
        {"_id": ObjectId(prescription_id)}
        if ObjectId.is_valid(prescription_id)
        else {"rx_code": prescription_id}
    )
    result = await prescriptions_collection.delete_one(query)
    return result.deleted_count > 0
