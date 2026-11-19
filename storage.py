import json
import os

from patient import Patient
from clinician import Clinician
from appointment import Appointment

DATA_FOLDER = "data"


class JSONStorage:
    def __init__(self, folder=DATA_FOLDER):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)   # make the folder if it's missing

    def _path(self, name):
        return os.path.join(self.folder, f"{name}.json")

    def _read_list(self, name):
        """Return the list stored in a file. Never crashes on a bad file."""
        path = self._path(name)

        if not os.path.exists(path):          # missing file -> start empty
            return []

        with open(path, "r") as file:
            text = file.read().strip()

        if text == "":                        # empty file -> start empty
            return []

        try:
            data = json.loads(text)
        except json.JSONDecodeError:          # malformed file -> keep a copy, start empty
            os.replace(path, path + ".bad")
            print(f"Warning: {name}.json was damaged. Saved a copy as {name}.json.bad")
            return []

        if not isinstance(data, list):        # valid JSON but wrong shape
            print(f"Warning: {name}.json has the wrong format. Starting empty.")
            return []

        return data

    def _write_list(self, name, items):
        with open(self._path(name), "w") as file:
            json.dump(items, file, indent=2)

    def save_all(self, patients, clinicians, appointments):
        self._write_list("patients", [p.to_dict() for p in patients.values()])
        self._write_list("clinicians", [c.to_dict() for c in clinicians.values()])
        self._write_list("appointments", [a.to_dict() for a in appointments])

    def load_all(self):
        patients = {}
        for record in self._read_list("patients"):
            try:
                patient = Patient(record["id"], record["name"],
                                  record["phone_number"], record["date_of_birth"])
                patients[patient.person_id] = patient
            except (KeyError, ValueError, AttributeError) as error:
                print(f"Skipped a bad patient record: {error}")

        clinicians = {}
        for record in self._read_list("clinicians"):
            try:
                clinician = Clinician(record["id"], record["name"],
                                      record["phone_number"], record["specialty"])
                clinicians[clinician.person_id] = clinician
            except (KeyError, ValueError, AttributeError) as error:
                print(f"Skipped a bad clinician record: {error}")

        appointments = []
        for record in self._read_list("appointments"):
            try:
                # Keep references valid: both people must exist
                if record["patient_id"] not in patients:
                    raise ValueError(f"unknown patient {record['patient_id']}")
                if record["clinician_id"] not in clinicians:
                    raise ValueError(f"unknown clinician {record['clinician_id']}")

                appointments.append(Appointment(
                    record["id"], record["patient_id"], record["clinician_id"],
                    record["date"], record["time"], record["purpose"],
                    record["status"]))
            except (KeyError, ValueError, AttributeError) as error:
                print(f"Skipped a bad appointment record: {error}")

        return patients, clinicians, appointments