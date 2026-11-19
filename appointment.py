from datetime import datetime, timedelta

#RULES
CLINIC_OPENING_HOUR = "08:30"
CLINIC_CLOSING_HOUR = "17:30"
SLOT_DURATION_MINUTES = 30

VALID_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
VALID_STATUSES = ["Scheduled", "Completed", "Cancelled"]


class Appointment:
    def __init__(self, appointment_id, patient_id, clinician_id, date, time, purpose, status="Scheduled"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.clinician_id = clinician_id
        self.set_when(date, time)
        self.purpose = purpose
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}.")
        self._status = value

    def set_when(self, date, time):
        """Checks if the date and time are real andwithin clinic hours."""
        try:
            start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            if start.strftime("%A") not in VALID_DAYS:
               raise ValueError(f"Appointments can only be scheduled on weekdays: {VALID_DAYS}.")
        except ValueError:
            raise ValueError("Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM' for time.")


        end = start + timedelta(minutes=SLOT_DURATION_MINUTES)
        opens = datetime.strptime(f"{date} {CLINIC_OPENING_HOUR}", "%Y-%m-%d %H:%M")
        closes = datetime.strptime(f"{date} {CLINIC_CLOSING_HOUR}", "%Y-%m-%d %H:%M")
        if start < opens or end > closes:
            raise ValueError(f"Lanterna is open from {CLINIC_OPENING_HOUR} to {CLINIC_CLOSING_HOUR}.")


        self._date = date
        self._time = time


    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    @property
    def start(self):
        return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")


    @property
    def end(self):
        return self.start + timedelta(minutes=SLOT_DURATION_MINUTES)

    def overlaps(self, other):
        """True if the two appointments share any time."""
        return self.start < other.end and other.start < self.end

    def is_active(self):
        return self.status == "Scheduled" 

    def cancel(self):
        self.status = "Cancelled"

    def complete(self):
        self.status = "Completed"

    def describe(self):
        return (f"{self.appointment_id}: {self.date} {self.time} | "
                f"patient {self.patient_id} with clinician {self.clinician_id} | "
                f"{self.purpose} [{self.status}]")

    def to_dict(self):
        return {
            "id": self.appointment_id,
            "patient_id": self.patient_id,
            "clinician_id": self.clinician_id,
            "date": self.date,
            "time": self.time,
            "purpose": self.purpose,
            "status": self.status

        }