from patient import Patient
from clinician import Clinician
from appointment import Appointment
from storage import JSONStorage

storage = JSONStorage("test_data")   # a separate folder, so real data stays safe

patients = {"P1": Patient("P1", "Peter Mugo", "0733930299", "2004-03-10")}
clinicians = {"D1": Clinician("D1", "William Muriuki", "0733930299", "Cardiologist")}
appointments = [Appointment("A1", "P1", "D1", "2026-11-23", "09:00", "Checkup")]

storage.save_all(patients, clinicians, appointments)

p, c, a = storage.load_all()
print("Loaded:", len(p), "patients,", len(c), "clinicians,", len(a), "appointments")
print(a[0].describe())

# Now damage the patients file on purpose
with open("test_data/patients.json", "w") as f:
    f.write("{this is not valid json")

p, c, a = storage.load_all()
print("After damage:", len(p), "patients,", len(c), "clinicians,", len(a), "appointments")