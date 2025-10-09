from bson import ObjectId
from DrugDispensorySystem.config.db import db

doctors_collection = db["doctors"]



async def get_doctor_by_id(doctor_id: str):

    if not doctor_id:
        print("[doctor_repository] doctor_id is missing or None")
        return None

    print(f" [doctor_repository] Searching for doctor_id: {doctor_id}")


    doctor = await doctors_collection.find_one({"_id": doctor_id})

    if doctor:
        print(f" [doctor_repository] Doctor found: {doctor.get('name')} ({doctor['_id']})")
    else:
        print(f" [doctor_repository] No doctor found for ID: {doctor_id}")


        doctor = await doctors_collection.find_one({"username": doctor_id})
        if doctor:
            print(f" [doctor_repository] Found by username fallback: {doctor.get('name')}")

    return doctor


async def create_doctor(doctor_data: dict):
    result = await doctors_collection.insert_one(doctor_data)
    return str(result.inserted_id)


async def get_all_doctors():
    cursor = doctors_collection.find({})
    doctors = await cursor.to_list(length=1000)
    for doctor in doctors:
        doctor["_id"] = str(doctor["_id"])
    return doctors


async def update_doctor(doctor_id: str, update_data: dict):
    query = {"_id": doctor_id}
    if ObjectId.is_valid(doctor_id):
        query = {"_id": ObjectId(doctor_id)}

    result = await doctors_collection.update_one(query, {"$set": update_data})
    return result.modified_count > 0


async def delete_doctor(doctor_id: str):
    query = {"_id": doctor_id}
    if ObjectId.is_valid(doctor_id):
        query = {"_id": ObjectId(doctor_id)}

    result = await doctors_collection.delete_one(query)
    return result.deleted_count > 0

