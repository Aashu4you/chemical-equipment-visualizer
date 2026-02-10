from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from styles import COLORS

class EquipmentView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Equipment List")
        title.setObjectName("Title")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        export_btn = QPushButton("Export PDF")
        export_btn.setFixedWidth(100)
        export_btn.setStyleSheet(f"background-color: {COLORS['primary']}; color: white;")
        export_btn.clicked.connect(self.export_pdf)
        header_layout.addWidget(export_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Flowrate", "Pressure", "Temperature"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_card']};
                gridline-color: {COLORS['border']};
                color: {COLORS['text_primary']};
                border: none;
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_darker']};
                color: {COLORS['text_secondary']};
                padding: 5px;
                border: none;
            }}
            QTableWidget::item {{
                padding: 10px;
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['bg_input']};
            }}
        """)
        
        layout.addWidget(self.table)
        
        # Load Data
        self.load_data()

    def load_data(self):
        response = self.api.get("equipment/")
        if response.status_code != 200:
            QMessageBox.warning(self, "Error", "Failed to fetch equipment list")
            return

        data = response.json()
        self.table.setRowCount(0)
        
        for row, item in enumerate(data):
            self.table.insertRow(row)
            
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(item.get("id"))))
            # Name
            self.table.setItem(row, 1, QTableWidgetItem(item.get("equipment_name", "")))
            # Type
            self.table.setItem(row, 2, QTableWidgetItem(item.get("equipment_type", "")))
            # Flow
            flow = QTableWidgetItem(f"{item.get('flowrate', 0):.2f}")
            flow.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, flow)
            # Pressure
            press = QTableWidgetItem(f"{item.get('pressure', 0):.2f}")
            press.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, press)
            # Temp
            temp = QTableWidgetItem(f"{item.get('temperature', 0):.2f}")
            temp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, temp)

    def export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        try:
            # We need to access API client properly
            # The APIClient.get returns a response object
            # We need to stream the content
            
            import requests # Need requests for streaming if APIClient doesn't expose it well, but APIClient uses requests
            
            # Use the existing API client's session/headers logic but we need raw content
            # Let's add a 'get_raw' or just use the token manually?
            # Or just use api.get and access response.content
            
            response = self.api.get("generate-pdf/", params={"type": "All"}) # Default filter
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                QMessageBox.information(self, "Success", f"PDF saved to {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to generate PDF")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

