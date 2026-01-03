import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QPlainTextEdit, QDialog, QHeaderView, QInputDialog)

from clinic.controller import Controller

from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.gui.note_dialog import NoteDialog
from clinic.gui.patient_dialog import PatientDialog
from datetime import datetime

class ClinicGUI(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.patient_table = QTableWidget(self) 
        self.setCentralWidget(self.patient_table)
     
        self.controller = Controller()
        self.setWindowTitle("Patient Management System")
        self.setGeometry(100, 100, 800, 600)
        
        # Create layouts for the main screens
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.init_login_screen()

    def init_login_screen(self):
        """Initializes the login screen layout."""
        self.clear_layout(self.main_layout)

        layout = QGridLayout()

        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button_login = QPushButton("Login")
        self.button_login.setStyleSheet("height: 30px;")
        self.button_quit = QPushButton("Quit")
        self.button_quit.setStyleSheet("height: 30px;")

        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.text_username, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.text_password, 1, 1)
        layout.addWidget(self.button_login, 2, 1)
        layout.addWidget(self.button_quit, 2, 0)

        self.main_layout.addLayout(layout)

        # Connect button signals
        self.button_login.clicked.connect(self.login_button_clicked)
        self.button_quit.clicked.connect(self.quit_button_clicked)

    def init_main_menu(self):
        """Initializes the main menu layout after login."""
        self.clear_layout(self.main_layout)

        layout = QVBoxLayout()

        label_welcome = QLabel("Welcome to your patient management system")
        label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_manage_patients = QPushButton("Manage Patients")
        button_manage_patients.setStyleSheet("height: 30px;")
        button_manage_notes = QPushButton("Manage Notes")
        button_manage_notes.setStyleSheet("height: 30px;")
        button_logout = QPushButton("Logout")
        button_logout.setStyleSheet("height: 30px;")

        layout.addWidget(label_welcome)
        layout.addWidget(button_manage_patients)
        layout.addWidget(button_logout)

        self.main_layout.addLayout(layout)

        # Connect buttons
        button_manage_patients.clicked.connect(self.manage_patients_clicked)
        button_logout.clicked.connect(self.logout_button_clicked)

    def login_button_clicked(self):
        ''' handles controller login '''
        username = self.text_username.text() 
        password = self.text_password.text()

        try:
            if self.controller.login(username, password):
                QMessageBox.information(self,"Succesfull", "Your login was succesfull.")
                self.init_main_menu()
        except InvalidLoginException:
            QMessageBox.warning(self,"Invalid", "Invalid login, please try again.")

        self.text_username.setText("")
        self.text_password.setText("")

    def logout_button_clicked(self):
        """Handles logout."""
        try:
            if self.controller.logout():
                QMessageBox.information(self, "Logged out", "You were succesfully logged out.")
                self.init_login_screen()
        except InvalidLogoutException:
            QMessageBox.warning(self, "Error", "Logout failed.")

    def quit_button_clicked(self):
        ''' quit the program '''
        QApplication.quit()

    def manage_patients_clicked(self):
        """Initializes the patient management screen."""
        self.clear_layout(self.main_layout)
        self.controller.unset_current_patient()

        layout_h = QHBoxLayout()
        layout = QVBoxLayout()
    
        label_manage_patients = QLabel("Manage Patients")
        label_manage_patients.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_patient_retrieve = QLabel("Search by name:")
        self.text_patient_retrieve = QLineEdit()
        button_patient_retrieve = QPushButton("Search")
        layout_h.addWidget(label_patient_retrieve)
        layout_h.addWidget(self.text_patient_retrieve)
        layout_h.addWidget(button_patient_retrieve)

        label_patient_search = QLabel("Search by PHN:")
        self.text_patient_search = QLineEdit()
        button_patient_search = QPushButton("Search")
        button_clear_search = QPushButton("Clear Search")
        layout_h.addWidget(label_patient_search)
        layout_h.addWidget(self.text_patient_search)
        layout_h.addWidget(button_patient_search)
        layout_h.addWidget(button_clear_search)

        # patient table
        self.patient_table = QTableWidget(0, 6)
        self.patient_table.setHorizontalHeaderLabels(["PHN", "Name", "Date of birth", "Phone #", "E-mail", "Address"])
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.refresh_patient_table()
        
        # init buttons
        button_add_patient = QPushButton("Add Patient")
        button_add_patient.setStyleSheet("height: 30px;")
        button_delete_patient = QPushButton("Delete Patient")
        button_delete_patient.setStyleSheet("height: 30px;")
        button_view_record = QPushButton("View Record")
        button_view_record.setStyleSheet("height: 30px;")
        button_back = QPushButton("Back")
        button_back.setStyleSheet("height: 30px;")
        button_edit_patient = QPushButton("Edit Patient")
        button_edit_patient.setStyleSheet("height: 30px;")
    
        # layout
        layout.addWidget(label_manage_patients)
        layout.addLayout(layout_h)
        layout.addWidget(self.patient_table)
        layout.addWidget(button_add_patient)
        layout.addWidget(button_delete_patient)
        layout.addWidget(button_edit_patient)
        layout.addWidget(button_view_record)
        layout.addWidget(button_back)

        self.main_layout.addLayout(layout)

        # connect buttons
        button_patient_retrieve.clicked.connect(self.retrieve_patients_clicked)
        button_patient_search.clicked.connect(self.search_patient_clicked)
        button_add_patient.clicked.connect(self.add_patient_clicked)
        button_delete_patient.clicked.connect(self.delete_patient_clicked)
        button_back.clicked.connect(self.init_main_menu)
        button_edit_patient.clicked.connect(self.edit_patient)
        button_clear_search.clicked.connect(self.clear_search_clicked)
        button_view_record.clicked.connect(self.view_record_clicked)

    def retrieve_patients_clicked(self):
        """Handles searching for a single patient by name."""
        search_name = self.text_patient_retrieve.text().strip()
        if not search_name:
            QMessageBox.warning(self, "Error", "Please enter a name to search.")
            #self.refresh_patient_table()
            return
        try:
            patients = self.controller.retrieve_patients(search_name)
            if len(patients) < 1:
                QMessageBox.information(self, "No Results", "No patients found with that name.")
            else:
                self.refresh_patient_table(patients)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {str(e)}")


    def search_patient_clicked(self):
        """Searches patients by PHN"""
        phn = self.text_patient_search.text().strip()
        if not phn:
            QMessageBox.warning(self, "Error", "Please enter a PHN to search")
            return
        patient_the = []
        patient = self.controller.search_patient(int(phn))
        patient_the.append(patient)
        try:
            if not patient:
                QMessageBox.information(self, "No Results", "No patient found with that PHN.")
            else:
                self.refresh_patient_table(patient_the)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {str(e)}")

    def clear_search_clicked(self):
        """clears the previous search"""
        self.refresh_patient_table()       

    def clear_layout(self, layout):
        """Clear all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()
            elif sublayout := item.layout():
                self.clear_layout(sublayout)  
            else:
                layout.removeItem(item) 

    def add_patient_clicked(self):
        """Handles adding a new patient."""
        dialog = PatientDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            phn, name, birth_date, phone, email, address = dialog.get_data()
            try:
                new_patient = self.controller.create_patient(phn, name, birth_date, phone, email, address)
                #self.patients.append(new_patient)
                self.refresh_patient_table()
                QMessageBox.information(self, "Success!", "Patient added.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def delete_patient_clicked(self):
        """Handles deleting a selected patient."""
        selected_row = self.patient_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return
        phn = self.patient_table.item(selected_row, 0).text()
        self.controller.delete_patient(int(phn))
        QMessageBox.information(self, "Success!", "Patient deleted.")
        self.refresh_patient_table()
        
    def edit_patient(self):
        """Handles editing an existing patient's details."""
        selected_row = self.patient_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return

        # Get the selected patient's details
        phn = self.patient_table.item(selected_row, 0).text()
        name = self.patient_table.item(selected_row, 1).text()
        birth_date = self.patient_table.item(selected_row, 2).text()
        phone = self.patient_table.item(selected_row, 3).text()
        email = self.patient_table.item(selected_row, 4).text()
        address = self.patient_table.item(selected_row, 5).text()

        # Create a dictionary with the patient's details
        patient_data = {"phn": phn, "name": name, "birth_date": birth_date, "phone": phone, "email": email, "address": address}
        print(patient_data)

        # Open the PatientDialog with the selected patient's details
        dialog = PatientDialog(patient=patient_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                updated_phn, updated_name, updated_dob, updated_phone, updated_email, updated_address = dialog.get_data()

                # Update the patient using the controller
                self.controller.update_patient(int(phn), int(updated_phn), updated_name, updated_dob, updated_phone, updated_email, updated_address)
                self.refresh_patient_table()
                QMessageBox.information(self, "Success", "Patient details updated successfully.")
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def list_patients(self):
        """Lists all patients"""
        return self.controller.list_patients()

    def view_record_clicked(self):
        """Main window layout for maneging patients"""
        selected_row = self.patient_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a patient.")
            return
        phn = self.patient_table.item(selected_row, 0).text()
        name = self.patient_table.item(selected_row, 1).text()
        self.controller.set_current_patient(int(phn))
        
        self.clear_layout(self.main_layout)

        layout = QVBoxLayout()
        layout_h = QHBoxLayout()

        label_welcome = QLabel(f"Patient #{phn}: {name}")
        label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label_note_retrieve = QLabel("Search by text:")
        self.text_note_retrieve = QLineEdit()
        button_note_retrieve = QPushButton("Search")
        layout_h.addWidget(label_note_retrieve)
        layout_h.addWidget(self.text_note_retrieve)
        layout_h.addWidget(button_note_retrieve)

        label_note_search = QLabel("Search by code:")
        self.text_note_search = QLineEdit()
        button_note_search = QPushButton("Search")
        button_clear_search_note = QPushButton("Clear Search")
        layout_h.addWidget(label_note_search)
        layout_h.addWidget(self.text_note_search)
        layout_h.addWidget(button_note_search)
        layout_h.addWidget(button_clear_search_note)
        
        self.note_box = QPlainTextEdit()

        button_manage_create_note = QPushButton("Create Note")
        button_manage_create_note.setStyleSheet("height: 30px;")
        button_manage_update_note = QPushButton("Update Note")
        button_manage_update_note.setStyleSheet("height: 30px;")
        button_manage_delete_note = QPushButton("Delete Note")
        button_manage_delete_note.setStyleSheet("height: 30px;")
        button_back = QPushButton("Back")
        button_back.setStyleSheet("height: 30px;")

        layout.addWidget(label_welcome)
        layout.addLayout(layout_h)
        layout.addWidget(self.note_box)
        layout.addWidget(button_manage_create_note)
        layout.addWidget(button_manage_update_note)
        layout.addWidget(button_manage_delete_note)
        layout.addWidget(button_back)

        self.main_layout.addLayout(layout)

        # Connect buttons
        button_manage_create_note.clicked.connect(self.create_note_clicked)
        button_manage_update_note.clicked.connect(self.update_note_clicked)
        button_manage_delete_note.clicked.connect(self.delete_note_clicked)
        button_back.clicked.connect(self.manage_patients_clicked)
        button_note_retrieve.clicked.connect(self.retrieve_notes_clicked)
        button_note_search.clicked.connect(self.search_note_clicked)
        button_clear_search_note.clicked.connect(self.clear_search_clicked_note)

        self.refresh_note_box()

    def clear_search_clicked_note(self):
        """Clears any searches"""
        self.refresh_note_box()

    def create_note_clicked(self):
        """Handles creating a new note for the current patient."""
        dialog = NoteDialog()  
        if dialog.exec() == QDialog.DialogCode.Accepted:
            note_text = dialog.get_data()  
            try:
                self.controller.create_note(note_text)
                self.refresh_note_box()
                QMessageBox.information(self, "Success", "Note created successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def retrieve_notes_clicked(self):
        """Retrieves and filters notes by text"""
        search_text = self.text_note_retrieve.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Error", "Please enter text to search.")
            return
        try:
            notes = self.controller.retrieve_notes(search_text)
            if len(notes) < 1:
                QMessageBox.information(self, "No Results", "No notes found with that text.")
            else:
                self.refresh_note_box(notes)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {str(e)}")


    def search_note_clicked(self):
        """Searches and filters notes by code"""
        search_code = self.text_note_search.text().strip()
        if not search_code:
            QMessageBox.warning(self, "Error", "Please enter a code to search.")
            return
        try:
            note = []
            note_the = self.controller.search_note(int(search_code))
            if note_the:
                note.append(note_the)
                self.refresh_note_box(note)

            else:
                QMessageBox.information(self, "No Results", "No notes found with that code.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {str(e)}")

    def update_note_clicked(self):
        """Allows editing an existing note by its code."""
        note_code, ok = QInputDialog.getInt(self, "Update Note", "Enter the code of the note you want to update:")
        if not ok:
            return 
        dialog = NoteDialog()
        if dialog.exec() == 1:  
            new_text = dialog.get_data()
            if not new_text.strip():
                QMessageBox.warning(self, "Error", "Note text cannot be empty.")
                return
            try:
                updated = self.controller.update_note(note_code, new_text)
                if not updated:
                    QMessageBox.warning(self, "Error", "Note code does not exist.")
                else:
                    self.refresh_note_box()
                    QMessageBox.information(self, "Success", "Note updated successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def delete_note_clicked(self):
        """Handles deleting a selected note for the current patient."""
        note_code, ok = QInputDialog.getInt(self, "Delete Note", "Enter the code of the note you want to delete:")
        if not ok: 
            return
        try:
            deleted = self.controller.delete_note(note_code)
            if not deleted:
                QMessageBox.warning(self, "Error", "Note with that code does not exist.")
            else:
                self.refresh_note_box()
                QMessageBox.information(self, "Success", f"Note with code {note_code} deleted successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def refresh_patient_table(self, patients=None):
        """Refreshes the patient table with current data from controller."""
        self.patient_table.setRowCount(0)
        if patients is None:
            patients = self.list_patients()

        for patient in patients:
            row_position = self.patient_table.rowCount()
            self.patient_table.insertRow(row_position)

            self.patient_table.setItem(row_position, 0, QTableWidgetItem(str(patient.phn))) 
            self.patient_table.setItem(row_position, 1, QTableWidgetItem(patient.name)) 
            self.patient_table.setItem(row_position, 2, QTableWidgetItem(patient.birth_date))
            self.patient_table.setItem(row_position, 3, QTableWidgetItem(patient.phone)) 
            self.patient_table.setItem(row_position, 4, QTableWidgetItem(patient.email)) 
            self.patient_table.setItem(row_position, 5, QTableWidgetItem(patient.address))
    
    def refresh_note_box(self, notes=None):
        """refreshes note box to display updated results"""
        self.note_box.clear()
        if notes is None:
            notes = self.controller.list_notes()
        for note in notes:
            time = datetime.strptime(str(note.timestamp), "%Y-%m-%d %H:%M:%S.%f")
            self.note_box.appendPlainText(f'(Note Code: {note.code}) "{note.text}" Date: {time}\n')

def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
