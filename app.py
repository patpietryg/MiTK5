from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog, QMainWindow, QTextEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox, QDialog, QLineEdit
import crypto

class App(QMainWindow):
    """
    Main application window for encrypting and decrypting text in images.
    """
    def __init__(self):
        """
        Initializes the main application window.
        """
        super().__init__()
        self.setWindowTitle("Aplikacja z polami tekstowymi i obrazkami")
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label_text = QLabel("Text to be encrypted")
        self.layout.addWidget((self.label_text))

        self.text_entry = QTextEdit()
        self.layout.addWidget(self.text_entry)

        self.label_text = QLabel("Shift")
        self.layout.addWidget((self.label_text))

        self.shift_entry = QTextEdit()
        self.shift_entry.resize(100,50)
        self.layout.addWidget(self.shift_entry)

        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.layout.addWidget(self.decrypt_button)

    def encrypt_text(self):
        """
        Encrypts the text using Caesar cipher and hides it in an image.
        """
        plaintext = self.text_entry.toPlainText()
        shift = self.shift_entry.toPlainText()

        if not shift.isdigit():
            QMessageBox.critical(self, "Error", "Shift must be an integer.")
            return

        shift = int(shift)

        file_path, _ = QFileDialog.getOpenFileName(self, "Choose image", "",
                                                   "Image Files (*.png *.jpg *.jpeg)")

        save_path, _ = QFileDialog.getSaveFileName(self, "Save the image with the encrypted text", "",
                                                   "Image Files (*.png *.jpg *.jpeg)")
        if not file_path:
            return

        encrypted_text = crypto.caesar_cipher_encrypt(plaintext, shift)
        info = crypto.hide_text_in_image(file_path, encrypted_text, save_path)

        QMessageBox.information(self, "Success", info)

    def decrypt_text(self):
        """
        Decrypts the text hidden in an image and displays the decrypted text.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose image", "", "Image Files (*.png *.jpg *.jpeg)")

        shift_dialog = ShiftDialog(self)
        if shift_dialog.exec_():
            shift = shift_dialog.get_shift()
            if not shift.isdigit():
                QMessageBox.critical(self, "Error", "Shift must be an integer.")
                return
            shift = int(shift)

            extracted_text = crypto.extract_text_from_image(file_path)
            decrypted_text = crypto.caesar_cipher_decrypt(extracted_text, shift)

            text_dialog = TextDialog(decrypted_text, self)
            text_dialog.exec_()

class ShiftDialog(QDialog):
    """
    Dialog window for entering the shift value.
    """
    def __init__(self, parent=None):
        """
        Initializes the ShiftDialog window.

        Args:
            parent (QWidget): The parent widget.
        """
        super().__init__(parent)

        self.setWindowTitle("Enter Shift")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter the shift value:")
        self.layout.addWidget(self.label)

        self.shift_entry = QLineEdit()
        self.layout.addWidget(self.shift_entry)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
    def get_shift(self):
        """
        Returns the entered shift value.

        Returns:
            str: The entered shift value.
        """
        return self.shift_entry.text()

class TextDialog(QDialog):
    """
    Dialog window for displaying decrypted text.
    """
    def __init__(self, text, parent=None):
        """
        Initializes the TextDialog window.

        Args:
            text (str): The decrypted text to display.
            parent (QWidget): The parent widget.
        """
        super().__init__(parent)

        self.setWindowTitle("Decrypted Text")
        self.layout = QVBoxLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)