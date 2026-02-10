from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

# Styles
from styles import COLORS

class StatCard(QFrame):
    def __init__(self, title, value, color_key="primary"):
        super().__init__()
        self.setObjectName("Card")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {COLORS['text_tertiary']}; font-size: 12px; font-weight: bold; text-transform: uppercase;")
        
        value_lbl = QLabel(str(value))
        value_lbl.setStyleSheet(f"color: {COLORS[color_key]}; font-size: 24px; font-weight: bold;")
        
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)

class OverviewView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Title
        title = QLabel("Dashboard Overview")
        title.setObjectName("Title")
        self.layout.addWidget(title)
        
        # Stats Grid
        self.stats_grid = QGridLayout()
        self.layout.addLayout(self.stats_grid)
        
        # Charts Area (Horizontal Layout)
        self.charts_layout = QHBoxLayout()
        self.layout.addLayout(self.charts_layout)
        
        # Load Data
        self.refresh_data()

    def refresh_data(self):
        # 1. Fetch Summary Stats
        print(f"DEBUG: Requesting summary from summary/")
        response_summary = self.api.get("summary/")
        
        if response_summary.status_code == 200:
            data = response_summary.json()
            
            # Clear existing stats
            while self.stats_grid.count():
                item = self.stats_grid.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            self.stats_grid.addWidget(StatCard("Total Equipment", data.get("total", 0)), 0, 0)
            self.stats_grid.addWidget(StatCard("Avg Flowrate", f"{data.get('avg_flow') or 0:.2f}", "secondary"), 0, 1)
            self.stats_grid.addWidget(StatCard("Avg Pressure", f"{data.get('avg_pressure') or 0:.2f}", "accent"), 0, 2)
            self.stats_grid.addWidget(StatCard("Avg Temp", f"{data.get('avg_temperature') or 0:.2f}", "primary"), 0, 3)
        
        # 2. Fetch All Equipment for detailed charts
        print(f"DEBUG: Requesting equipment list for charts")
        response_eq = self.api.get("equipment/")
        if response_eq.status_code == 200:
            equipment_list = response_eq.json()
            if equipment_list:
                df = pd.DataFrame(equipment_list)
                self.plot_charts(df)
            else:
                self.show_error("No data available for charts")
        else:
            self.show_error("Failed to load equipment data")

    def plot_charts(self, df):
        # Clear previous charts
        while self.charts_layout.count():
            item = self.charts_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Common Style
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'

        # --- Chart 1: Pie Chart (Distribution) ---
        fig1 = Figure(figsize=(4, 3), dpi=100)
        fig1.patch.set_facecolor(COLORS['bg_card'])
        ax1 = fig1.add_subplot(111)
        ax1.set_facecolor(COLORS['bg_card'])
        
        if not df.empty and 'equipment_type' in df.columns:
            dist = df['equipment_type'].value_counts()
            colors = ['#0066ff', '#00d9ff', '#ff3366', '#00ff88', '#a0aec0']
            
            wedges, texts, autotexts = ax1.pie(
                dist, labels=dist.index, autopct='%1.1f%%',
                startangle=90, colors=colors[:len(dist)],
                textprops=dict(color="white")
            )
            ax1.set_title("Equipment Types", color="white")
        
        canvas1 = FigureCanvasQTAgg(fig1)
        canvas1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.charts_layout.addWidget(canvas1)

        # --- Chart 2: Bar Chart (Avg Flowrate by Type) ---
        fig2 = Figure(figsize=(4, 3), dpi=100)
        fig2.patch.set_facecolor(COLORS['bg_card'])
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor(COLORS['bg_card'])

        if not df.empty and 'equipment_type' in df.columns and 'flowrate' in df.columns:
            # Ensure flowrate is numeric
            df['flowrate'] = pd.to_numeric(df['flowrate'], errors='coerce')
            avg_flow_by_type = df.groupby('equipment_type')['flowrate'].mean()
            
            ax2.bar(avg_flow_by_type.index, avg_flow_by_type.values, color=COLORS['secondary'])
            ax2.set_title("Avg Flowrate by Type", color="white")
            ax2.tick_params(axis='x', rotation=45)
        
        canvas2 = FigureCanvasQTAgg(fig2)
        canvas2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.charts_layout.addWidget(canvas2)

        # --- Chart 3: Scatter Plot (Flow vs Pressure) ---
        fig3 = Figure(figsize=(4, 3), dpi=100)
        fig3.patch.set_facecolor(COLORS['bg_card'])
        ax3 = fig3.add_subplot(111)
        ax3.set_facecolor(COLORS['bg_card'])

        if not df.empty and 'flowrate' in df.columns and 'pressure' in df.columns:
             # Ensure numeric
            df['flowrate'] = pd.to_numeric(df['flowrate'], errors='coerce')
            df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')
            
            ax3.scatter(df['flowrate'], df['pressure'], color=COLORS['accent'], alpha=0.7)
            ax3.set_title("Flow vs Pressure", color="white")
            ax3.set_xlabel("Flowrate")
            ax3.set_ylabel("Pressure")
        
        canvas3 = FigureCanvasQTAgg(fig3)
        canvas3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.charts_layout.addWidget(canvas3)

    def show_error(self, msg):
        err = QLabel(msg)
        err.setStyleSheet("color: red;")
        self.layout.addWidget(err)
