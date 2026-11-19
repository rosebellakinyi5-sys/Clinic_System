from patient import Patient
from clinician import Clinician 
from appointment_manager import AppointmentManager


patients = {
    "P1": Patient("P1", "Peter Mugo", "0733930299", "2004-03-10"),
    "P2": Patient("P2", "Alice Wanjiku", "0754321098", "2000-01-01"),
}

clinicians = {
    "D1": Clinician("D1", "William Muriuki", "0799043786", "Cardiologist"),
    "D2": Clinician("D2", "Nathan Karanja", "0723456789", "Dermatologist"),
}

manager = AppointmentManager([], patients, clinicians)

def attempt(label, action):
    try:
        result = action()
        print(label, "-> OK:", result.describe() if result else "done")
    except ValueError as error:
        print(label, "-> BLOCKED:", error)


attempt("1 book P1 with D1 at 09:00", lambda: manager.schedule("P1", "D1", "2026-06-15", "09:00", "Checkup"))
attempt("2 book P2 with D1 at 09:15", lambda: manager.schedule("P2", "D1", "2026-06-15", "09:15", "Follow-up"))
attempt("3 book P2 with D1 at 09:30", lambda: manager.schedule("P2", "D2", "2026-06-15", "09:30", "Follow-up"))
attempt("4 unknown patient P9", lambda: manager.schedule("P9", "D1", "2026-06-15", "11:00", "Test"))


manager.cancel("A1")
attempt("5 book P2 with D1 at 09:00 after cancelling A1", lambda: manager.schedule("P2", "D1", "2026-06-15", "09:00", "Checkup"))
attempt("6 reschedule A3 to 10:00", lambda: manager.reschedule("A3", "2026-06-15", "10:00"))


print()
for appt in manager.on_date("2026-06-15"):
    print(appt.describe())

print(manager.daily_summary("2026-06-15"))