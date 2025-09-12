from DrugDispensorySystem.Repository import prescription_repository
from DrugDispensorySystem.utils.rx_code_generator import generate_rx_code


async def create_prescription(prescription_data: dict):
    prescription_data["rx_code"] = generate_rx_code()
    return await prescription_repository.create_prescription(prescription_data)

async def get_prescription_by_id(prescription_id: str):
    prescription = await prescription_repository.get_prescription_by_id(prescription_id)
    if not prescription:
        raise ValueError("Prescription not found")
    return prescription

async def get_prescriptions_by_patient(patient_id: str):
    return await prescription_repository.get_prescriptions_by_patient(patient_id)

async def update_prescription(prescription_id: str, update_data: dict):
    success = await prescription_repository.update_prescription(prescription_id, update_data)
    if not success:
        raise ValueError("Failed to update prescription")
    return True
