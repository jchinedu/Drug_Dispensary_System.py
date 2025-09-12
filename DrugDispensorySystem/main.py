from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DrugDispensorySystem.controller import auth_controller, doctor_controller, pharmacist_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_controller.router)
app.include_router(doctor_controller.router)
app.include_router(pharmacist_controller.router)

@app.get("/")
async def root():
    return {"message": "Drug Dispensary API is running 🚀"}
