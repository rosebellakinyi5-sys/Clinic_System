from patient import Patient
from clinician import Clinician

pat = Patient("P1", "Peter Mugo", "0733930299", "2004-03-10")
doc = Clinician("D1", "William Muriuki", "0733930299", "Cardiologist")

print(pat.describe())
print(doc.describe())
print(pat.to_dict())

try:
    bad = Patient("P2", "   ", "321", "2002-05-01")
except ValueError as error:
    print("Caught:", error)
    
