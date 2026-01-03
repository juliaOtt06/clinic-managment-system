from clinic.patient_record import PatientRecord
from typing import Union, List
from clinic.note import Note

class Patient:
    def __init__(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str, autosave=False):
        """Initialize a Patient with personal and contact details, and create an associated patient record."""
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.patient_record = PatientRecord(autosave, phn)

    def __eq__(self, other) -> bool:
        """Check equality between this Patient and another based on personal details."""
        if not isinstance(other, Patient):
            return False
        if (self.phn == other.phn and
                self.name == other.name and
                self.birth_date == other.birth_date and
                self.phone == other.phone and
                self.email == other.email and 
                self.address == other.address):
            return True
        
    def __repr__(self) -> str:
        """Return a string representation of the Patient."""
        return f"Patient({self.phn}, {self.name}, {self.birth_date}, {self.phone}, {self.email}, {self.address})"
    
    def create_note(self, text: str) -> Union[Note,None]:
        """Create a new note in the patient's record with the provided text."""
        return self.patient_record.create_note(text)
    
    def search_note(self, code: int) -> Union[Note,None]: 
        """Search for a note in the patient's record by its code."""
        return self.patient_record.search_note(code)

    def retrieve_notes(self, text: str) -> List[Note]:
        """Retrieve all notes in the patient's record that contain the specified text."""
        return self.patient_record.retrieve_notes(text)

    def update_note(self, code: int, new_text: str) -> bool:
        """Update the text of an existing note in the patient's record by code."""
        return self.patient_record.update_note(code, new_text)
    
    def delete_note(self, code: int) -> bool:
        """Delete a note from the patient's record by code."""
        return self.patient_record.delete_note(code)
      
    def list_notes(self) -> List[Note]:
        """List all notes in the patient's record from newest to oldest."""
        return self.patient_record.list_notes()