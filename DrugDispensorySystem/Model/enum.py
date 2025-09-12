from enum import Enum

class DrugType(str, Enum):
    TABLET = "Tablet"
    CAPSULE = "Capsule"
    SYRUP = "Syrup"
    INJECTION = "Injection"
    INHALER = "Inhaler"
    OTHERS = "Others"
