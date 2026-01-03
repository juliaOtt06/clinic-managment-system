from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QDialogButtonBox

class NoteDialog(QDialog):
    def __init__(self, note=None):
        super().__init__()
        self.setWindowTitle("Add/Edit Note")
        self.setModal(True)

        self.layout = QVBoxLayout(self)
        self.input_note = QPlainTextEdit(self)

        if note:
            self.input_note.setPlainText(note)

        self.layout.addWidget(self.input_note)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_data(self):
        """Returns the note text from the dialog."""
        return self.input_note.toPlainText()



