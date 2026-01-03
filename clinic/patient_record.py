from datetime import datetime
from clinic.note import Note
from typing import List, Union
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self, autosave, phn):
        self.note_dao = NoteDAOPickle(autosave)
        if autosave:
            self.note_dao.load_notes(phn)

    def create_note(self, text: str) -> Note:
       """Create a new note for the current patient."""
       return self.note_dao.create_note(text)

    def search_note(self, code: str) -> Union[Note, None]:
        """Search for a note by code."""
        return self.note_dao.search_note(code)

    def retrieve_notes(self, text: str) -> List[Note]:
        """Retrieve notes by text search."""
        return self.note_dao.retrieve_notes(text)

    def update_note(self, code: int, new_text: str) -> bool:
        """Update a note's text."""
        return self.note_dao.update_note(code, new_text)

    def delete_note(self, code: str) -> bool:
        """Delete a note by code.""" 
        return self.note_dao.delete_note(code)

    def list_notes(self) -> List[Note]:
       """List all notes for the current patient from newest to oldest.""" 
       return self.note_dao.list_notes()


    