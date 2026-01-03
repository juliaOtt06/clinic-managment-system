from datetime import datetime

class Note:
    def __init__(self, code: int, text: str, timestamp: datetime =None):
        """ Initialize a Note with a unique code, text, and an optional timestamp.
        If no timestamp is provided, the current time is used."""
        self.code = code
        self.text = text
        self.timestamp = timestamp or datetime.now()

    def __eq__(self, other) -> bool:
        """Compare this Note with another to check for equality based on code and text."""
        if not isinstance(other, Note):
            return False
        if (self.code == other.code and
                self.text == other.text):
            return True
        
    def __repr__(self) -> str:
        """Return a string representation of the Note."""
        return f"Note({self.code}, {self.text}, {self.timestamp})"
    