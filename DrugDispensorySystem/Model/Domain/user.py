from DrugDispensorySystem.Model.user import UserRole


class User:
    def __init__(self, id, username, full_name, role, password):
        self._id = id
        self._username = username
        self._full_name = full_name
        self._role = role
        self._password = password

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, UserRole):
            raise ValueError("role must be a UserRole Enum")
        self._role = value


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def __str__(self):
        return (
            f"User(id={self.id}, username= {self.username}, full_name= {self.full_name}, "
            f"role={self.role}, password='****')"
        )
