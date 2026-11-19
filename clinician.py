from person import Person

class Clinician(Person):
    def __init__(self, person_id, name, phone_number, specialty):
        super().__init__(person_id, name, phone_number)
        self.specialty = specialty

    def describe(self):
        return f"Dr. {self.name} ({self.person_id}), {self.specialty}, phone: {self.phone_number}"

    def to_dict(self):
        data = super().to_dict()
        data["specialty"] = self.specialty
        return data