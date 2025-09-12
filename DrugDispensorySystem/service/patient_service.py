from DrugDispensorySystem.Repository import patient_repository


async def create_patient(patient_data: dict):
    return await patient_repository.create_patient(patient_data)

async def get_patient_by_id(patient_id: str):
    patient = await patient_repository.get_patient_by_id(patient_id)
    if not patient:
        raise ValueError("Patient not found")
    return patient

async def get_all_patients():
    return await patient_repository.get_all_patients()

async def update_patient(patient_id: str, update_data: dict):
    success = await patient_repository.update_patient(patient_id, update_data)
    if not success:
        raise ValueError("Failed to update patient")
    return True
