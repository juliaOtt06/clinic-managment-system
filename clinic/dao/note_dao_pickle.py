from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
from datetime import datetime
from pickle import load, dump
from typing import Optional, List

class NoteDAOPickle(NoteDAO):
    def __init__(self, autosave=False):
        self.autosave = autosave
        self.notes = []
        self.autocounter = 0
        self.filename = ''

    def load_notes(self, phn: int):
        """Loads notes of patient with given phn"""
        self.filename = f'clinic/records/{phn}.dat'
        try:
            with open(self.filename, 'rb') as file:
                self.notes = load(file)
            self.autocounter = self.notes[-1].code if self.notes else 0
        except FileNotFoundError:
            self.notes = []
            self.autocounter = 0
        
    def dump_notes(self):
        """Save current notes"""
        with open(self.filename, 'wb') as file:
            dump(self.notes, file)
    
    def create_note(self, text: str) -> Note:
        """Create a new note for the current patient."""
        self.autocounter += 1
        new_note = Note(self.autocounter, text, datetime.now())
        self.notes.append(new_note)
        if self.autosave:
            self.dump_notes()
        return new_note
    
    def search_note(self, key: int) -> Optional[Note]:
        """Search for a note by code."""
        for note in self.notes:
            if int(note.code) == key:
                return note
        return None 
        
    def retrieve_notes(self, search_string: str) -> List[Note]:
        """Retrieve notes by text search."""
        retrieved_notes = []
        for note in self.notes:
            if search_string.lower() in note.text.lower():
                retrieved_notes.append(note)
        return retrieved_notes
    
    def update_note(self, key: int, text: str) -> bool:
        """Update a note's text."""
        note = self.search_note(key)
        if note:
            note.text = text
            note.timestamp = datetime.now()
            if self.autosave:
                self.dump_notes()
            return True
        return False

    def delete_note(self, key: int) -> bool:
        """Delete a note by code."""
        note = self.search_note(key)
        if note:
            self.notes.remove(note)
            if self.autosave:
                self.dump_notes()
            return True
        return False
    
    def list_notes(self) -> List[Note]:
        """List all notes for the current patient from newest to oldest."""
        lo_notes = []
        for note in range(len(self.notes)-1, -1, -1):
            lo_notes.append(self.notes[note])
        return lo_notes
    
