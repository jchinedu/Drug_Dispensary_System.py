class Patient:
    def __init__(self, id, name, age, diagnosis):
        self._id = id
        self._name = name
        self._age = age
        self._diagnosis = diagnosis


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age


    @property
    def diagnosis(self):
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, diagnosis):
        self._diagnosis = diagnosis


    def __str__(self):
        return (f"Patient(id={self.id}, name= {self.name}, "
                f"age={self.age}, diagnosis='{self.diagnosis}')")
