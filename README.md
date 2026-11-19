# Lanterna Clinic Appointment Management System

A command-line program for a small clinic to manage patients, clinicians and appointments. Clinic staff can book, move and cancel appointments, and the system stops a clinician from being double-booked.

## Features

- **Patients:** register, view, search and update patients
- **Clinicians:** register, view, search (by name, ID or specialty) and update clinicians
- **Appointments:** schedule, reschedule, cancel and mark as completed
- **Conflict prevention:** a clinician cannot be booked for overlapping appointments
- **Validation:** clinic hours 08:30-17:30, weekdays only, 30-minute slots, no bookings in the past, valid names and phone numbers (at least 10 digits)
- **Reports:** appointments for a patient, a clinician's schedule, appointments on a date, and a daily summary
- **Persistence:** all data is saved in JSON files and reloaded on startup, and missing, empty or damaged files are handled without crashing
- **Decorators:** `@log_action` writes every scheduling action to `clinic_log.txt`, and `@time_it` times the daily summary report

## How to use

Run `python3 main.py` to open the main menu. Choose Patients, Clinicians, Appointments or Reports, and each opens its own submenu. To book an appointment, choose Appointments, then Schedule, and enter the patient ID, clinician ID, date (YYYY-MM-DD), time (HH:MM) and purpose. If the clinician already has an appointment at that time, the program shows an error and nothing is saved. Everything is saved automatically after each change, and `0` goes back or exits.

IDs are created automatically: patients are `P1`, `P2`..., clinicians are `D1`, `D2`..., and appointments are `A1`, `A2`...

## Project structure

| File | Purpose |
|------|---------|
| `person.py` | `Person` base class with validated name and phone number |
| `patient.py` | `Patient`, inherits from `Person`, adds date of birth |
| `clinician.py` | `Clinician`, inherits from `Person`, adds specialty |
| `appointment.py` | `Appointment` with status, time validation and overlap check |
| `appointment_manager.py` | Scheduling rules, conflict detection and report queries |
| `decorators.py` | `log_action` and `time_it` decorators |
| `storage.py` | `JSONStorage`: loading and saving, with handling for bad files |
| `clinic.py` | `Clinic` coordinates patients, clinicians and the manager |
| `main.py` | The interactive menu |
| `seed_data.py` | Creates the sample data |
| `data/` | The JSON files for patients, clinicians and appointments |
| `test_*.py` | Small scripts used to test each part |

## Design decisions

Appointments store only the patient and clinician IDs, not the whole objects, so the JSON stays simple and the details are always looked up from the one place they are stored. Validation lives inside the classes, so bad data is rejected no matter which part of the program sends it. Storage is a separate class so the file handling can change without touching the scheduling rules. The menu in `main.py` only talks to the user, and the rules live in the other classes.
