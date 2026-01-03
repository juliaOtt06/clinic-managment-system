from clinic.patient import Patient
from clinic.note import Note
from clinic.patient_record import PatientRecord
from datetime import datetime
from typing import List
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle
import hashlib

class Controller:
  def __init__(self, autosave=True):
    """Initializes the Controller for managing user authentication and patient records."""
    self._logged_in = False
    self.patients = {}
    self.autocounter = 0
    self.autosave = autosave
    self.patient_dao = PatientDAOJSON(autosave)
    self.users = self.load_users()

  def _is_logged_in(self) -> bool:
    """Check is the user is logged in."""
    return self._logged_in
    
  def _patient_exists(self, phn: int) -> bool:
    """Check if a patient exists in the records."""
    try:
      self.patient_dao.search_patient(phn)
      return True
    except IllegalOperationException:
      return False
  
  def load_users(self):
    """Load users from file into a dictionary. Users are predefined if autosave is False."""
    users = {}
    if not self.autosave:
      users = {
        'user': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
        'ali': '6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810',
        'kala': 'e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e'
        }
    else:
      try:
          with open('clinic/users.txt', 'r') as file:
              for line in file:
                  username, password_hash = line.strip().split(',')
                  users[username] = password_hash
      except FileNotFoundError:
          print("uh oh!")
    return users

  def get_password_hash(self, password):
    """gets and returns hexadecimal digest of a hashed password"""
    encoded_password = password.encode('utf-8')     # Convert the password to bytes
    hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
    hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
    return hex_dig

  def login(self, username: str, password: str) -> bool:
    """Log in the user."""
    if self._logged_in:
        raise DuplicateLoginException
    if self.users.get(username):
      password_hash = self.get_password_hash(password)
      if self.users.get(username) == password_hash:
        self._logged_in = True
        return True
      else:
        raise InvalidLoginException
    else:
      raise InvalidLoginException
    
  def logout(self) -> bool:
    """Log out the user."""
    if not self._is_logged_in():
      raise InvalidLogoutException
    self._logged_in = False
    return True
  
  def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str
  ) -> Patient:
    """Create a new patient record."""
    if not self._is_logged_in():
      raise IllegalAccessException
    try:
      if self.patient_dao.search_patient(phn):
        raise IllegalOperationException
    except IllegalOperationException:
      pass
    return self.patient_dao.create_patient(phn, name, birth_date, phone, email, address)
  
  def search_patient(self, phn: int) -> Patient:
    """Search for a patient by phn."""
    if not self._is_logged_in():
        raise IllegalAccessException
    return self.patient_dao.search_patient(phn)

  def retrieve_patients(self, name: str) -> List[Patient]:
    """Retrieve patients by name."""
    if not self._is_logged_in():
      raise IllegalAccessException
    return self.patient_dao.retrieve_patients(name)

  def update_patient(self, phn: int, new_phn: str, new_name: str, new_birth_date: str, new_phone: str, 
  new_email: str, new_address: str) -> bool:
    """Update a patient's details."""
    if not self._is_logged_in():
      raise IllegalAccessException
    if not self._patient_exists(phn):
      raise IllegalOperationException
    return self.patient_dao.update_patient(phn, new_phn, new_name, new_birth_date, new_phone, new_email, new_address)
  
  def delete_patient(self, phn: int) -> bool:
    """Delete a patient's record."""
    if not self._is_logged_in():
      raise IllegalAccessException
    if not self._patient_exists(phn):
      raise IllegalOperationException
    self.patient_dao.delete_patient(phn)
    return True

  def list_patients(self) -> List[Patient]:
    """List all patients."""
    if not self._is_logged_in():
      raise IllegalAccessException
    return self.patient_dao.list_patients()

  def set_current_patient(self, phn: int) -> None:
    """Set the current active patient."""
    if not self._is_logged_in():
      raise IllegalAccessException
    return self.patient_dao.set_current_patient(phn)

  def get_current_patient(self):
    """Get the current patient."""
    if not self._is_logged_in():
      raise IllegalAccessException
    return self.patient_dao.get_current_patient()

  def unset_current_patient(self) -> None:
    """Unset the current patient."""
    if not self._is_logged_in():
      raise IllegalAccessException
    return self.patient_dao.unset_current_patient()

  def create_note(self, text: str) -> Note:
    """Create a new note for the current patient."""
    if not self._is_logged_in():
      raise IllegalAccessException
    if self.patient_dao.get_current_patient() == None:
      raise NoCurrentPatientException
    return self.patient_dao.get_current_patient().create_note(text)
  
  def search_note(self, code: int) -> Note: 
    """Search for a note by code."""
    if not self._is_logged_in():
      raise IllegalAccessException
    current_patient = self.patient_dao.get_current_patient()
    if not current_patient:
      raise NoCurrentPatientException
    note = current_patient.patient_record.search_note(code)
    return note
    
  def retrieve_notes(self, text: str) -> List[Note]:
    """Retrieve notes by text search."""
    if not self._is_logged_in():
      raise IllegalAccessException

    current_patient = self.patient_dao.get_current_patient()

    if not current_patient:
      raise NoCurrentPatientException
    return current_patient.patient_record.retrieve_notes(text)

  def update_note(self, code: int, new_text: str) -> bool:
    """Update a note's text."""
    if not self._is_logged_in():
      raise IllegalAccessException
    current_patient = self.patient_dao.get_current_patient()
    if not current_patient:
      raise NoCurrentPatientException
    return current_patient.update_note(code, new_text)
  
  def delete_note(self, code: int) -> bool:
    """Delete a note by code."""
    if not self._is_logged_in():
      raise IllegalAccessException
    current_patient = self.patient_dao.get_current_patient()
    if not current_patient:
      raise NoCurrentPatientException

    return current_patient.delete_note(code)
    
  def list_notes(self) -> List[Note]:
    """List all notes for the current patient from newest to oldest."""
    if not self._is_logged_in():
      raise IllegalAccessException
    current_patient = self.patient_dao.get_current_patient()
    if not current_patient:
      raise NoCurrentPatientException
    return current_patient.patient_record.list_notes()

  


