from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QFormLayout, QMessageBox

class PatientDialog(QDialog):
    """Dialog for adding/editing a patient."""
    def __init__(self, patient=None):
        super().__init__()
        self.setWindowTitle("Add/Edit Patient")
        self.setModal(True)

        self.layout = QFormLayout(self)

        self.input_phn = QLineEdit(self)
        self.input_name = QLineEdit(self)
        self.input_dob = QLineEdit(self)
        self.input_phone = QLineEdit(self)
        self.input_email = QLineEdit(self)
        self.input_address = QLineEdit(self)

        if patient:
            self.input_phn.setText(patient.get("phn", ""))
            self.input_name.setText(patient.get("name", ""))
            self.input_dob.setText(patient.get("birth_date", ""))
            self.input_phone.setText(patient.get("phone", ""))
            self.input_email.setText(patient.get("email", ""))
            self.input_address.setText(patient.get("address", ""))

        self.layout.addRow("PHN:", self.input_phn)
        self.layout.addRow("Name:", self.input_name)
        self.layout.addRow("Date of Birth:", self.input_dob)
        self.layout.addRow("Phone #:", self.input_phone)
        self.layout.addRow("E-mail:", self.input_email)
        self.layout.addRow("Address:", self.input_address)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_data(self):
        """Returns data from the dialog as a dictionary."""
        try:
            phn = int(self.input_phn.text())  # Convert to integer
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "PHN must be a number.")
            return None  # Return None if PHN is invalid
        name = self.input_name.text()
        dob = self.input_dob.text()
        phone = self.input_phone.text()
        email = self.input_email.text()
        address = self.input_address.text()
        return phn, name, dob, phone, email, address