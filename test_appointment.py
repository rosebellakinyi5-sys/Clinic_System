from appointment import Appointment

a1 = Appointment("A1", "P1", "D1", "2026-06-15", "10:00", "Checkup")
a2 = Appointment("A2", "P2", "D1", "2026-06-15", "10:30", "Follow-up")
a3 = Appointment("A3", "P3", "D1", "2026-06-15", "11:00", "Review")

print(a1.describe())
print("a1 and a2 overlap:", a1.overlaps(a2))
print("a1 and a3 overlap:", a1.overlaps(a3))

a1.cancel()
print(a1.status)

try:
    Appointment("A4", "P1", "D1", "2026-06-15", "18:00", "Late visit")
except ValueError as error:
    print("Caught:", error)

try:
    Appointment("A5", "P1", "D1", "15-06-2026", "09:00", "Wrong format")
except ValueError as error:
    print("Caught:", error)
