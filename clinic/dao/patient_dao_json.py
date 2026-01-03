import json
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.dao.note_dao_pickle import NoteDAOPickle 
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
from typing import Optional, List


class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave=False):
        self.filename = 'clinic/patients.json'
        self.autosave = autosave
        if self.autosave:
            try:
                with open(self.filename, 'r') as file:
                    self._patients = json.load(file, cls=PatientDecoder)
            except (FileNotFoundError, json.JSONDecodeError):
                self._patients = {}
        else:
            self._patients = {}
        self.current_patient = None

    def dump_json(self):
        """Save patients when autosave is True"""
        if self.autosave:
            with open(self.filename, 'w') as file:
                json.dump(self._patients, file, cls=PatientEncoder)
  
    def search_patient(self, phn: int) -> Optional[Patient]:
        """Retrieve a single patient by PHN."""
        if self.autosave:
            phn = str(phn)
        if phn in self._patients:
            patient = self._patients[phn]
            return patient
        
        return None
        
    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, 
        email: str, address: str) -> Patient:
        """Add a new patient to the collection."""
        new_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)

        patient_phn = new_patient.phn
        if self.autosave:
            patient_phn = str(patient_phn)

        if self.search_patient(patient_phn) == None:
            self._patients[new_patient.phn] = new_patient
            self.dump_json()
        else:
            raise IllegalOperationException("PHN already exists.")
        return new_patient

    def retrieve_patients(self, search_string: str) -> List[Patient]:
        """Retrieve patients matching a name substring."""
        retrived_patients = []
        for patient in self._patients.values():
            if search_string.lower() in patient.name.lower():
                retrived_patients.append(patient)
        self.dump_json()
        return retrived_patients

    def update_patient(self, old_phn: int, new_phn: str, new_name: str, new_birth_date: str, new_phone: str, 
        new_email: str, new_address: str) -> bool:
        """Update an existing patient."""
        if self.autosave:
            _new_phn = str(new_phn)
            _old_phn = str(old_phn)
        else:
            _new_phn = new_phn
            _old_phn = old_phn

        if self.current_patient != None and self.current_patient.phn == old_phn: 
            raise IllegalOperationException
        if old_phn != new_phn:
            if _new_phn in self._patients: 
                raise IllegalOperationException
        if _old_phn not in self._patients: 
            raise IllegalOperationException

        patient = self.search_patient(old_phn)

        patient.phn = new_phn
        patient.name = new_name
        patient.birth_date = new_birth_date
        patient.phone = new_phone
        patient.email = new_email
        patient.address = new_address

        self.delete_patient(old_phn)
        self._patients[_new_phn] = patient
        self.dump_json()
        return True

    def delete_patient(self, key: int):
        """Remove a patient from the collection."""
        if self.autosave:
            key = str(key)

        
        print(f"Attempting to delete patient with key: {key}")
        keys = list(self._patients.keys())
        print(f"Available keys in _patients: {keys} of type {type(keys[0])}")
        
            
        if key not in self._patients:
            print(f"Error: Key {key} not found in _patients.")              
            raise IllegalOperationException
        if self._patients[key] == self.current_patient:
            raise IllegalOperationException
        del self._patients[key]
        self.dump_json()

    def list_patients(self) -> List[Patient]:
        """List all patients."""
        return list(self._patients.values())

    def set_current_patient(self, phn: int) -> bool:
        """Set a current patient"""
        phn = str(phn)
        for patient in self._patients.values():
            if int(patient.phn) == int(phn):
                self.current_patient = patient
                return True
        raise IllegalOperationException

    def get_current_patient(self) -> Optional[Patient]:
        """Return the current patient"""
        return self.current_patient
        
    def unset_current_patient(self):
        """Unset the current patient"""
        self.current_patient = None