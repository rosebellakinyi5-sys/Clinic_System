from datetime import datetime

from patient import Patient
from clinician import Clinician
from appointment_manager import AppointmentManager
from storage import JSONStorage


class Clinic:
    def __init__(self, name="Lanterna Clinic", storage=None):
        self.name = name
        self.storage = storage or JSONStorage()
        patients, clinicians, appointments = self.storage.load_all()
        self.patients = patients
        self.clinicians = clinicians
        # The manager shares the SAME dictionaries, so new people are seen instantly
        self.manager = AppointmentManager(appointments, self.patients, self.clinicians)

    @staticmethod
    def _next_id(prefix, existing_ids):
        numbers = [int(i[len(prefix):]) for i in existing_ids]
        return f"{prefix}{max(numbers, default=0) + 1}"

    # ---- patients ----
    def add_patient(self, name, phone, date_of_birth):
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date of birth must look like YYYY-MM-DD.")
        patient_id = self._next_id("P", self.patients.keys())
        patient = Patient(patient_id, name, phone, date_of_birth)  # setters validate
        self.patients[patient_id] = patient
        return patient

    def get_patient(self, patient_id):
        if patient_id not in self.patients:
            raise ValueError(f"No patient found with ID {patient_id}.")
        return self.patients[patient_id]

    def search_patients(self, text):
        text = text.lower()
        return [p for p in self.patients.values()
                if text in p.name.lower() or text == p.person_id.lower()]

    def update_patient(self, patient_id, name=None, phone=None):
        patient = self.get_patient(patient_id)
        if name:
            patient.name = name
        if phone:
            patient.phone_number = phone
        return patient

    # ---- clinicians ----
    def add_clinician(self, name, phone, specialty):
        if not specialty.strip():
            raise ValueError("Specialty cannot be empty.")
        clinician_id = self._next_id("D", self.clinicians.keys())
        clinician = Clinician(clinician_id, name, phone, specialty.strip())
        self.clinicians[clinician_id] = clinician
        return clinician

    def get_clinician(self, clinician_id):
        if clinician_id not in self.clinicians:
            raise ValueError(f"No clinician found with ID {clinician_id}.")
        return self.clinicians[clinician_id]

    def search_clinicians(self, text):
        text = text.lower()
        return [c for c in self.clinicians.values()
                if text in c.name.lower() or text in c.specialty.lower()
                or text == c.person_id.lower()]

    def update_clinician(self, clinician_id, name=None, phone=None, specialty=None):
        clinician = self.get_clinician(clinician_id)
        if name:
            clinician.name = name
        if phone:
            clinician.phone_number = phone
        if specialty:
            clinician.specialty = specialty
        return clinician

    # ---- saving ----
    def save(self):
        self.storage.save_all(self.patients, self.clinicians, self.manager.appointments)