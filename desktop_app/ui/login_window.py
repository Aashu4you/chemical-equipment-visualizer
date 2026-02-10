from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from api_client import APIClient

class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.api = APIClient()
        self.init_ui()

    def init_ui(self):
        # Main Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)

        # Card Frame
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel("Welcome Back")
        title_label.setObjectName("Title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Sign in to access your dashboard")
        subtitle_label.setObjectName("Subtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle_label)
        
        card_layout.addSpacing(20)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        card_layout.addWidget(self.email_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        card_layout.addSpacing(10)

        # Login Button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)

        # Add Card to Main Layout
        layout.addWidget(card)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        signup_label = QLabel("Don't have an account?")
        signup_label.setStyleSheet("color: #718096;")
        
        # Signup link (just a label for now, or could be a button)
        # If we had a signup page, we woud link it here
        
        layout.addLayout(footer_layout)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter both email and password.")
            return

        self.login_btn.setText("Signing in...")
        self.login_btn.setEnabled(False)
        self.repaint() # Force UI update

        success, message = self.api.login(email, password)

        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In")

        if success:
            # Navigate to Dashboard
            self.main_window.show_dashboard()
        else:
            QMessageBox.critical(self, "Login Failed", message)
