from DrugDispensorySystem.Model.Domain.user import User
from DrugDispensorySystem.Model.user import UserRole
from DrugDispensorySystem.service import auth_service


def test_verify_password():
    password = "123456"
    hashed = auth_service.hash_password(password)

    assert auth_service.verify_password(password, hashed) is True
    assert auth_service.verify_password("wrong", hashed) is False

def test_create_token():
    user = User(
        id="u1", username="doctor1", full_name="Dr. Jane",
        role=UserRole.DOCTOR, password="123456"
    )
    token = auth_service.create_access_token(user)
    assert isinstance(token, str)
