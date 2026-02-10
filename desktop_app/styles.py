
# Enhanced color palette for modern, attractive UI
COLORS = {
    "primary": "#0066ff",
    "primary_dark": "#0052cc",
    "primary_light": "#3385ff",
    "secondary": "#00d9ff",
    "accent": "#ff3366",
    "success": "#00ff88",
    "warning": "#ffaa00",
    
    "bg_dark": "#0a0e17",
    "bg_darker": "#050810",
    "bg_card": "#1a2332",
    "bg_card_hover": "#1f2937",
    "bg_input": "#1a2332",
    
    "text_primary": "#ffffff",
    "text_secondary": "#a0aec0",
    "text_tertiary": "#718096",
    
    "border": "rgba(255, 255, 255, 0.1)",
    "border_light": "rgba(255, 255, 255, 0.05)",
    "shadow": "rgba(0, 0, 0, 0.3)",
}

def get_stylesheet():
    return f"""
    QMainWindow {{
        background-color: {COLORS['bg_dark']};
    }}
    
    QWidget {{
        color: {COLORS['text_primary']};
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
    }}

    /* QLabel */
    QLabel {{
        color: {COLORS['text_primary']};
    }}
    QLabel#Title {{
        font-size: 24px;
        font-weight: bold;
        color: {COLORS['text_primary']};
    }}
    QLabel#Subtitle {{
        font-size: 14px;
        color: {COLORS['text_secondary']};
    }}

    /* QLineEdit */
    QLineEdit {{
        background-color: {COLORS['bg_input']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 10px;
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['primary']};
    }}
    QLineEdit:focus {{
        border: 1px solid {COLORS['primary']};
    }}

    /* QPushButton */
    QPushButton {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary_dark']};
        padding-top: 13px; /* slight press effect */
    }}
    QPushButton:disabled {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_tertiary']};
    }}
    
    /* Secondary/Ghost Button */
    QPushButton#GhostButton {{
        background-color: transparent;
        border: 1px solid {COLORS['border']};
        color: {COLORS['text_secondary']};
    }}
    QPushButton#GhostButton:hover {{
        border: 1px solid {COLORS['primary']};
        color: {COLORS['primary']};
    }}

    /* QFrame (Cards) */
    QFrame#Card {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
    }}\r\n    \r\n    /* Stat Cards */\r\n    QFrame#StatCard {{\r\n        background-color: {COLORS['bg_card']};\r\n        border: 1px solid {COLORS['border']};\r\n        border-radius: 12px;\r\n    }}\r\n    """
