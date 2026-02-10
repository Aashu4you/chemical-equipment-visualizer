import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon

from styles import get_stylesheet
from ui.login_window import LoginWindow
# from ui.dashboard_window import DashboardWindow # Implement later

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemViz - Chemical Equipment Visualizer")
        self.resize(1280, 800)
        
        # Apply Global Styles
        self.setStyleSheet(get_stylesheet())

        # Central Stack for Navigation
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize Views
        self.login_view = LoginWindow(self)
        # self.dashboard_view = DashboardWindow(self) 

        self.stack.addWidget(self.login_view)
        # self.stack.addWidget(self.dashboard_view)

        # Start at Login
        self.show_login()

    def show_login(self):
        self.stack.setCurrentWidget(self.login_view)

    def show_dashboard(self):
        # Lazy load dashboard to ensure token is ready
        from ui.dashboard_window import DashboardWindow
        self.dashboard_view = DashboardWindow(self)
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentWidget(self.dashboard_view)
        # remove login view from stack if desired, or keep for logout

    def logout(self):
        # Clear token (handled in API client usually, or here)
        from api_client import APIClient
        APIClient().token = None
        
        # Go back to login
        self.stack.setCurrentWidget(self.login_view)
        # Optional: cleanup dashboard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
