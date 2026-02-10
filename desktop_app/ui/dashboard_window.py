from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon

from styles import COLORS
from api_client import APIClient
from ui.upload_dialog import UploadDialog
from ui.overview_view import OverviewView
from ui.equipment_view import EquipmentView

class DashboardWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.api = APIClient()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet(f"background-color: {COLORS['bg_darker']}; border-right: 1px solid {COLORS['border']};")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo Area
        logo_frame = QFrame()
        logo_frame.setFixedHeight(80)
        logo_layout = QHBoxLayout(logo_frame)
        logo_label = QLabel("CHEM VIS")
        logo_label.setStyleSheet(f"color: {COLORS['primary']}; font-size: 20px; font-weight: bold; font-family: 'Courier New';")
        logo_layout.addWidget(logo_label)
        sidebar_layout.addWidget(logo_frame)

        # Navigation List
        self.nav_list = QListWidget()
        self.nav_list.setFrameShape(QFrame.Shape.NoFrame)
        self.nav_list.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                height: 50px;
                padding-left: 20px;
                color: {COLORS['text_secondary']};
                border-left: 3px solid transparent;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['primary']};
                border-left: 3px solid {COLORS['primary']};
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
            }}
        """)
        
        self.add_nav_item("Overview")
        self.add_nav_item("Equipment")
        self.add_nav_item("Upload CSV") 
        
        self.nav_list.currentRowChanged.connect(self.change_page)
        sidebar_layout.addWidget(self.nav_list)
        
        sidebar_layout.addStretch()

        # Logout Button
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("GhostButton")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.main_window.logout)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar_layout.addSpacing(20)

        main_layout.addWidget(sidebar)

        # --- Main Content Area ---
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # Pages
        self.overview_view = OverviewView(self.api)
        self.equipment_view = EquipmentView(self.api)
        
        self.content_stack.addWidget(self.overview_view)
        self.content_stack.addWidget(self.equipment_view)
        
    def add_nav_item(self, name):
        item = QListWidgetItem(name)
        self.nav_list.addItem(item)

    def change_page(self, index):
        if index == 2: # Upload CSV
            dialog = UploadDialog(self, self.api)
            if dialog.exec(): # If uploaded successfully
                # Refresh data
                self.overview_view.refresh_data()
                self.equipment_view.load_data()
                # Switch to Overview or keep current?
                # Let's go to Overview to show new stats
                self.nav_list.setCurrentRow(0)
            else:
                # Restore selection to previous if cancelled
                pass # logic to revert selection would be complex, just stay where we are or let list item sit
                # Better: Don't change the stack index for 'Upload', just launch dialog.
           
            # Reset selection to avoid showing empty page if we didn't switch
            if self.content_stack.currentIndex() != 2:
                 self.nav_list.blockSignals(True)
                 self.nav_list.setCurrentRow(self.content_stack.currentIndex())
                 self.nav_list.blockSignals(False)
            return

        self.content_stack.setCurrentIndex(index)
