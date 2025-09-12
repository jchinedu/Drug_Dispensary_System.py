class Drug:
    def __init__(self, id, name, quantity, drug_type, days_to_use):
        self._id = id
        self._name = name
        self._quantity = quantity
        self._drug_type = drug_type
        self._days_to_use = days_to_use

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def drug_type(self):
        return self._drug_type

    @drug_type.setter
    def drug_type(self, value):
        self._drug_type = value

    @property
    def days_to_use(self):
        return self._days_to_use

    @days_to_use.setter
    def days_to_use(self, value):
       self._days_to_use = value

    def __str__(self):
        return (f"Drug(id={self.id}, name= {self.name}, "
                f"quantity={self.quantity}, type= {self.drug_type}, "
                f"days_to_use={self.days_to_use})")
