from decorators import log_action, time_it
from appointment import Appointment
from datetime import datetime

class AppointmentManager:
    def __init__(self, appointments, patients, clinicians):
        self.appointments = appointments
        self.patients = patients
        self.clinicians = clinicians

    def next_id(self):
        """A1, A2, A3... one higher than the biggest existing number."""
        numbers = [int(a.appointment_id[1:]) for a in self.appointments]
        return f"A{max(numbers, default=0) + 1}"


    def find(self, appointment_id):
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                return appt
        raise ValueError(f"No appointment found with ID {appointment_id}.")

    def check_conflict(self,  clinician_id, new_appt, ignore_id=None):
        """Raise an error if this Clinician is busy at the same time."""
        for existing in self.appointments:
            if existing.clinician_id != clinician_id:
                continue
            if not existing.is_active():
                continue
            if existing.appointment_id == ignore_id:
                continue
            if existing.overlaps(new_appt):
                raise ValueError(
                    f"Clinician {clinician_id} is already booked " 
                    f"{existing.time} on {existing.date}."  
                )                              

    @log_action
    def schedule(self, patient_id, clinician_id, date, time, purpose):
        if patient_id not in self.patients:
            raise ValueError(f"No patient found with ID {patient_id}.")
        if clinician_id not in self.clinicians:
            raise ValueError(f"No clinician found with ID {clinician_id}.")

        new_appt = Appointment(self.next_id(), patient_id, clinician_id, date, time, purpose)
        if new_appt.start < datetime.now():
            raise ValueError("Cannot schedule an appointment in the past.")
        self.check_conflict(clinician_id, new_appt)
        self.appointments.append(new_appt)
        return new_appt
    

    @log_action
    def cancel(self, appointment_id):
        appt = self.find(appointment_id)
        if not appt.is_active():
            raise ValueError(f"Only scheduled appointments can be cancelled.")
        appt.cancel()

    @time_it
    def daily_summary(self, date):
        todays = self.on_date(date)
        return {
            "date": date,
            "total": len(todays),
            "scheduled": len([a for a in todays if a.status == "Scheduled"]),
            "completed": len([a for a in todays if a.status == "Completed"]),
            "cancelled": len([a for a in todays if a.status == "Cancelled"]),
        }

    @log_action
    def reschedule(self, appointment_id, new_date, new_time):
        appt = self.find(appointment_id)
        if not appt.is_active():
            raise ValueError(f"Only scheduled appointments can be rescheduled.")

        trial = Appointment("TEMP", appt.patient_id, appt.clinician_id, new_date, new_time, appt.purpose)
        if trial.start < datetime.now():
            raise ValueError("Cannot reschedule an appointment to the past.")
        self.check_conflict(appt.clinician_id, trial, ignore_id=appointment_id)
        appt.set_when(new_date, new_time)
    

    #Queries
    def for_patient(self, patient_id):
        return [a for a in self.appointments if a.patient_id == patient_id]

    def for_clinician(self, clinician_id):
        return [a for a in self.appointments if a.clinician_id == clinician_id]

    def on_date(self, date):
        return [a for a in self.appointments if a.date == date]

    @log_action
    def complete(self, appointment_id):
        appt = self.find(appointment_id)
        if not appt.is_active():
            raise ValueError(f"Only scheduled appointments can be completed.")
        appt.complete()