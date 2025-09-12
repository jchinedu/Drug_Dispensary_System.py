from DrugDispensorySystem.config.db import db

users_collection = db["users"]

async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)

async def get_user_by_username(username: str):
    return await users_collection.find_one({"username": username})

async def get_user_by_id(user_id: str):
    from bson import ObjectId
    return await users_collection.find_one({"_id": ObjectId(user_id)})
