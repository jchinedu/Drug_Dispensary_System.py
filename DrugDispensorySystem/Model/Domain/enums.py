from enum import Enum


class DrugType(Enum):
    TABLET = "Tablet"
    CAPSULE = "Capsule"
    SYRUP = "Syrup"
    INJECTION = "Injection"
    INHALER = "Inhaler"
    OTHERS = "Others"

class UserRole(Enum):
        DOCTOR = "doctor"
        PHARMACIST = "pharmacist"