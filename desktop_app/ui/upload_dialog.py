from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt
from styles import COLORS

class UploadDialog(QDialog):
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self.api = api_client
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Upload CSV")
        self.setFixedSize(400, 250)
        self.setStyleSheet(f"background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']};")

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Upload Equipment Data")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLORS['text_primary']}; border: none;")
        layout.addWidget(title)

        # File Selection File
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet(f"color: {COLORS['text_secondary']}; border: none;")
        layout.addWidget(self.file_label)

        # Select Button
        self.select_btn = QPushButton("Select CSV File")
        self.select_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_btn)

        # Progress Bar (Hidden initially)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
            }}
        """)
        layout.addWidget(self.progress)

        # Upload Button
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet(f"background-color: {COLORS['secondary']}; color: black;")
        layout.addWidget(self.upload_btn)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path.split("/")[-1])
            self.upload_btn.setEnabled(True)

    def upload_file(self):
        if not self.file_path:
            return

        self.progress.setVisible(True)
        self.progress.setRange(0, 0) # Indeterminate
        self.select_btn.setEnabled(False)
        self.upload_btn.setEnabled(False)
        self.repaint()

        try:
            with open(self.file_path, 'rb') as f:
                # Prepare headers inside api_client usually, need to make sure we don't send JSON content type
                # Our APIClient.post handles `files` argument by popping Content-Type
                
                print(f"DEBUG: Uploading to upload/")
                response = self.api.post("upload/", files={'file': f})
                
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "File uploaded successfully!")
                self.accept() # Close dialog
            else:
                QMessageBox.critical(self, "Upload Failed", response.json().get("error", "Unknown error"))
                self.reset_ui()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reset_ui()

    def reset_ui(self):
        self.progress.setVisible(False)
        self.select_btn.setEnabled(True)
        self.upload_btn.setEnabled(True)
