from clinic import Clinic


def ask(prompt):
    """Keep asking until the person types something."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def ask_id(prompt):
    return ask(prompt).upper()          # so "p1" works the same as "P1"


def show_people(people):
    if not people:
        print("Nothing found.")
    for person in people:
        print("  ", person.describe())


def show_appointments(appointments):
    if not appointments:
        print("No appointments found.")
        return
    ordered = sorted(appointments, key=lambda a: (a.date, a.time))
    active = [a for a in ordered if a.is_active()]
    closed = [a for a in ordered if not a.is_active()]
    print("ACTIVE:")
    for a in active:
        print("  ", a.describe())
    if not active:
        print("   (none)")
    print("COMPLETED / CANCELLED:")
    for a in closed:
        print("  ", a.describe())
    if not closed:
        print("   (none)")


def patient_menu(clinic):
    while True:
        print("\n--- Patients ---")
        print("1. Register patient")
        print("2. View all patients")
        print("3. Search patients")
        print("4. Update patient")
        print("0. Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                patient = clinic.add_patient(ask("Name: "), ask("Phone: "),
                                             ask("Date of birth (YYYY-MM-DD): "))
                clinic.save()
                print("Registered:", patient.describe())
            elif choice == "2":
                show_people(clinic.patients.values())
            elif choice == "3":
                show_people(clinic.search_patients(ask("Search by name or ID: ")))
            elif choice == "4":
                pid = ask_id("Patient ID: ")
                clinic.get_patient(pid)
                name = input("New name (Enter to keep): ").strip()
                phone = input("New phone (Enter to keep): ").strip()
                updated = clinic.update_patient(pid, name, phone)
                clinic.save()
                print("Updated:", updated.describe())
            elif choice == "0":
                return
            else:
                print("Please choose a number from the menu.")
        except ValueError as error:
            print("Error:", error)


def clinician_menu(clinic):
    while True:
        print("\n--- Clinicians ---")
        print("1. Register clinician")
        print("2. View all clinicians")
        print("3. Search clinicians (name, ID or specialty)")
        print("4. Update clinician")
        print("0. Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                clinician = clinic.add_clinician(ask("Name: "), ask("Phone: "),
                                                 ask("Specialty: "))
                clinic.save()
                print("Registered:", clinician.describe())
            elif choice == "2":
                show_people(clinic.clinicians.values())
            elif choice == "3":
                show_people(clinic.search_clinicians(ask("Search: ")))
            elif choice == "4":
                cid = ask_id("Clinician ID: ")
                clinic.get_clinician(cid)
                name = input("New name (Enter to keep): ").strip()
                phone = input("New phone (Enter to keep): ").strip()
                specialty = input("New specialty (Enter to keep): ").strip()
                updated = clinic.update_clinician(cid, name, phone, specialty)
                clinic.save()
                print("Updated:", updated.describe())
            elif choice == "0":
                return
            else:
                print("Please choose a number from the menu.")
        except ValueError as error:
            print("Error:", error)


def appointment_menu(clinic):
    manager = clinic.manager
    while True:
        print("\n--- Appointments ---")
        print("1. Schedule appointment")
        print("2. Reschedule appointment")
        print("3. Cancel appointment")
        print("4. Mark appointment completed")
        print("0. Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                appt = manager.schedule(ask_id("Patient ID: "), ask_id("Clinician ID: "),
                                        ask("Date (YYYY-MM-DD): "),
                                        ask("Time (HH:MM, 24-hour): "),
                                        ask("Purpose: "))
                clinic.save()
                print("Booked:", appt.describe())
            elif choice == "2":
                manager.reschedule(ask_id("Appointment ID: "),
                                   ask("New date (YYYY-MM-DD): "),
                                   ask("New time (HH:MM): "))
                clinic.save()
                print("Appointment rescheduled.")
            elif choice == "3":
                manager.cancel(ask_id("Appointment ID: "))
                clinic.save()
                print("Appointment cancelled.")
            elif choice == "4":
                manager.complete(ask_id("Appointment ID: "))
                clinic.save()
                print("Appointment marked as completed.")
            elif choice == "0":
                return
            else:
                print("Please choose a number from the menu.")
        except ValueError as error:
            print("Error:", error)


def report_menu(clinic):
    manager = clinic.manager
    while True:
        print("\n--- Reports ---")
        print("1. Appointments for a patient")
        print("2. A clinician's schedule")
        print("3. Appointments on a date")
        print("4. Daily summary")
        print("0. Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                pid = ask_id("Patient ID: ")
                clinic.get_patient(pid)
                show_appointments(manager.for_patient(pid))
            elif choice == "2":
                cid = ask_id("Clinician ID: ")
                clinic.get_clinician(cid)
                show_appointments(manager.for_clinician(cid))
            elif choice == "3":
                show_appointments(manager.on_date(ask("Date (YYYY-MM-DD): ")))
            elif choice == "4":
                summary = manager.daily_summary(ask("Date (YYYY-MM-DD): "))
                print(f"Summary for {summary['date']}: {summary['total']} total | "
                      f"{summary['scheduled']} scheduled | "
                      f"{summary['completed']} completed | "
                      f"{summary['cancelled']} cancelled")
            elif choice == "0":
                return
            else:
                print("Please choose a number from the menu.")
        except ValueError as error:
            print("Error:", error)


def main():
    clinic = Clinic()
    print(f"Welcome to {clinic.name}")
    while True:
        print("\n=== LANTERNA CLINIC ===")
        print("1. Patients")
        print("2. Clinicians")
        print("3. Appointments")
        print("4. Reports")
        print("0. Save and exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            patient_menu(clinic)
        elif choice == "2":
            clinician_menu(clinic)
        elif choice == "3":
            appointment_menu(clinic)
        elif choice == "4":
            report_menu(clinic)
        elif choice == "0":
            clinic.save()
            print("Everything saved. Goodbye!")
            break
        else:
            print("Please choose a number from the menu.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Goodbye!")