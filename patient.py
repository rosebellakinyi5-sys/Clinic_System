from person import Person


class Patient(Person):
    def __init__(self, person_id, name, phone_number, date_of_birth):
        super().__init__(person_id, name, phone_number)
        self.date_of_birth = date_of_birth

    def describe(self):
        return f"Patient: {super().describe()} Date of Birth: {self.date_of_birth}"

    def to_dict(self):
        data = super().to_dict()
        data["date_of_birth"] = self.date_of_birth
        return data
