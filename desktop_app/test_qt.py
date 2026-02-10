from PyQt6.QtWidgets import QApplication, QLabel
import sys
try:
    app = QApplication(sys.argv)
    label = QLabel("Hello")
    print("PyQt6 Initialized Successfully")
except Exception as e:
    print(f"PyQt6 Error: {e}")
