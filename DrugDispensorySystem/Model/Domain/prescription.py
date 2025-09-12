class Prescription:
    def __init__(self, code, created_by_doctor_username, created_at, patient,
                 drugs, status, dispensed_by_pharmacist, dispensed_at, pharmacist_remarks):
        self._code = code
        self._created_by_doctor_username = created_by_doctor_username
        self._created_at = created_at
        self._patient = patient
        self._drugs = drugs
        self._status = status
        self._dispensed_by_pharmacist = dispensed_by_pharmacist
        self._dispensed_at = dispensed_at
        self._pharmacist_remarks = pharmacist_remarks


    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def created_by_doctor_username(self):
        return self._created_by_doctor_username

    @created_by_doctor_username.setter
    def created_by_doctor_username(self, value):
        self._created_by_doctor_username = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, value):
        self._patient = value

    @property
    def drugs(self):
        return self._drugs

    @drugs.setter
    def drugs(self, value):
        self._drugs = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def dispensed_by_pharmacist(self):
        return self._dispensed_by_pharmacist

    @dispensed_by_pharmacist.setter
    def dispensed_by_pharmacist(self, value):
        self._dispensed_by_pharmacist = value

    @property
    def dispensed_at(self):
        return self._dispensed_at

    @dispensed_at.setter
    def dispensed_at(self, value):
        self._dispensed_at = value

    @property
    def pharmacist_remarks(self):
        return self._pharmacist_remarks

    @pharmacist_remarks.setter
    def pharmacist_remarks(self, value):
        self._pharmacist_remarks = value

    def __str__(self):
        drugs_str = "\n    ".join([str(drug) for drug in self._drugs])
        return (
            f"Prescription(code= {self.code},\n"
            f"  created_by_doctor= {self.created_by_doctor_username},\n"
            f"  created_at={self.created_at},\n"
            f"  patient={self.patient},\n"
            f"  drugs=[\n    {drugs_str}\n  ],\n"
            f"  status= {self.status},\n"
            f"  dispensed_by_pharmacist= {self.dispensed_by_pharmacist},\n"
            f"  dispensed_at={self.dispensed_at},\n"
            f"  pharmacist_remarks= {self.pharmacist_remarks})"
        )
