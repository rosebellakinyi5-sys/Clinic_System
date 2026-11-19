class Person:
    def __init__(self, person_id, name, phone_number):
        self.person_id = person_id
        self.name = name
        self.phone_number = phone_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = value.strip()  
        if value == "":
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        value = value.strip()
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Phone number must be at least 10 digits and contain only numbers.")
        self._phone_number = value

    def describe(self):
        return f"{self.name} ({self.person_id}), phone: {self.phone_number}"

    def to_dict(self):
        return {"id": self.person_id, "name": self.name, "phone_number": self.phone_number}
    