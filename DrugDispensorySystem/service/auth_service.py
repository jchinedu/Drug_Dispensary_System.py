from passlib.hash import bcrypt
from uuid import uuid4
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from DrugDispensorySystem.config.db import db

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class AuthService:
    @staticmethod
    async def register_user(user_data: dict) -> str:
        username = user_data["username"]
        password = user_data["password"]
        role = user_data.get("role", "doctor")

        existing = await db.users.find_one({"username": username})
        if existing:
            raise ValueError("User already exists")

        hashed_pw = bcrypt.hash(password)
        user_id = str(uuid4())

        await db.users.insert_one({
            "_id": user_id,
            "username": username,
            "password": hashed_pw,
            "role": role
        })

        return user_id

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[str]:
        user = await db.users.find_one({"username": username})
        if not user:
            return None

        if not bcrypt.verify(password, user["password"]):
            return None


        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user["_id"]),
            "username": user["username"],
            "role": user["role"],
            "exp": expire
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return token
