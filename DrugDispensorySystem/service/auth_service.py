from passlib.hash import bcrypt
from uuid import uuid4
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from DrugDispensorySystem.config.db import db

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    @staticmethod
    async def register_user(user_data: dict) -> str:
        name = user_data["name"]
        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]
        confirm_password = user_data["confirm_password"]
        role = user_data.get("role", "doctor")
        if password != confirm_password:
            raise ValueError("Passwords do not match")

        existing = await db.users.find_one({"username": username})
        if existing:
            raise ValueError("User already exists")

        hashed_pw = bcrypt.hash(password)
        user_id = str(uuid4())

        await db.users.insert_one({
            "_id": user_id,
            "name": name,
            "username": username,
            "email": email,
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



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        role: str = payload.get("role")

        if user_id is None or username is None or role is None:
            raise credentials_exception

        # Verify user still exists in database
        user = await db.users.find_one({"_id": user_id})
        if user is None:
            raise credentials_exception

        return {
            "user_id": user_id,
            "username": username,
            "role": role
        }
    except JWTError:
        raise credentials_exception