# DrugDispensorySystem/controller/auth_controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from DrugDispensorySystem.service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register_user(data: RegisterRequest):
    try:
        user_id = await AuthService.register_user(data.dict())
        return {"user_id": user_id, "message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_user(data: LoginRequest):
    token = await AuthService.authenticate_user(data.username, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": token,
        "token_type": "bearer"
    }
