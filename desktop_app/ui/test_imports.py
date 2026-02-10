import sys
import os

# Add parent directory to path to simulate running from main.py's context if needed, 
# but usually running as module handles this. 
# We will run this file directly from desktop_app as: python -m ui.test_imports

try:
    from styles import COLORS
    print("Styles Import: OK")
except Exception as e:
    print(f"Styles Import Error: {e}")

try:
    from api_client import APIClient
    print("APIClient Import: OK")
except Exception as e:
    print(f"APIClient Import Error: {e}")
