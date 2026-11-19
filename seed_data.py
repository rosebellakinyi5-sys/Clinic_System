from clinic import Clinic

clinic = Clinic()

# Change these names to whatever you like. They are only sample data.
clinic.add_patient("Abigael Wambui", "0734298022", "2000-09-03")
clinic.add_patient("Peter Mugo", "0733930299", "2004-03-10")
clinic.add_patient("Amina Wanjiru", "0712345678", "1999-07-21")

clinic.add_clinician("William Muriuki", "0722111222", "Cardiology")
clinic.add_clinician("Brian Otieno", "0723456789", "General Practice")

m = clinic.manager
m.schedule("P1", "D1", "2026-11-23", "09:00", "Heart checkup")
m.schedule("P2", "D2", "2026-11-23", "09:30", "Flu symptoms")
m.schedule("P3", "D1", "2026-11-24", "10:00", "Follow-up")
m.schedule("P2", "D1", "2026-11-24", "11:00", "Blood pressure review")
m.cancel("A4")        # leaves a cancelled example
m.complete("A1")      # leaves a completed example

clinic.save()
print("Sample data saved.")