from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import fastapi.encoders

from DrugDispensorySystem.controller import auth_controller, doctor_controller, pharmacist_controller

app = FastAPI(title="Drug Dispensary API")


original_jsonable_encoder = jsonable_encoder

def custom_jsonable_encoder(obj, **kwargs):
    if isinstance(obj, ObjectId):
        return str(obj)
    return original_jsonable_encoder(obj, **kwargs)

fastapi.encoders.jsonable_encoder = custom_jsonable_encoder

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(doctor_controller.router)
app.include_router(pharmacist_controller.router)

@app.on_event("startup")
async def startup_event():
    print(" Drug Dispensary System API started successfully!")