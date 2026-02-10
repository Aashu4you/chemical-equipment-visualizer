from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QSizePolicy, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

# Styles
from styles import COLORS

class StatCard(QFrame):
    def __init__(self, title, value, color_key="primary", icon=None):
        super().__init__()
        self.setObjectName("StatCard")
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Left side - Icon/Color indicator
        indicator = QFrame()
        indicator.setFixedSize(4, 50)
        indicator.setStyleSheet(f"background-color: {COLORS[color_key]}; border-radius: 2px;")
        layout.addWidget(indicator)
        
        # Right side - Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)
        
        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet(f"color: {COLORS['text_tertiary']}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        
        value_lbl = QLabel(str(value))
        value_lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 32px; font-weight: 700; letter-spacing: -1px;")
        
        content_layout.addWidget(title_lbl)
        content_layout.addWidget(value_lbl)
        content_layout.addStretch()
        
        layout.addLayout(content_layout)
        layout.addStretch()

class ChartCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        header = QLabel(title)
        header.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: 600;")
        layout.addWidget(header)
        
        # Chart container
        self.chart_container = QVBoxLayout()
        layout.addLayout(self.chart_container)
        
    def set_chart(self, canvas):
        # Clear existing
        while self.chart_container.count():
            item = self.chart_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.chart_container.addWidget(canvas)

class OverviewView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.init_ui()

    def init_ui(self):
        # Main scroll area for the entire dashboard
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"QScrollArea {{ background-color: {COLORS['bg_dark']}; border: none; }}")
        
        # Container widget
        container = QWidget()
        container.setStyleSheet(f"QWidget {{ background-color: {COLORS['bg_dark']}; }}")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(24)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Dashboard Overview")
        title.setObjectName("Title")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        self.layout.addLayout(header_layout)
        
        # Stats Grid - 4 columns
        self.stats_container = QGridLayout()
        self.stats_container.setSpacing(16)
        self.layout.addLayout(self.stats_container)
        
        # Charts Section
        charts_header = QLabel("Analytics")
        charts_header.setObjectName("Heading")
        self.layout.addWidget(charts_header)
        
        # Charts Grid - 2 rows x 2 columns for better organization
        self.charts_grid = QGridLayout()
        self.charts_grid.setSpacing(16)
        self.layout.addLayout(self.charts_grid)
        
        self.layout.addStretch()
        
        # Set scroll area
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        # Load Data
        self.refresh_data()

    def refresh_data(self):
        # 1. Fetch Summary Stats
        print(f"DEBUG: Requesting summary from summary/")
        response_summary = self.api.get("summary/")
        
        if response_summary.status_code == 200:
            data = response_summary.json()
            
            # Clear existing stats
            while self.stats_container.count():
                item = self.stats_container.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Add stat cards in a 4-column grid
            self.stats_container.addWidget(
                StatCard("Total Equipment", data.get("total", 0), "primary"), 0, 0
            )
            self.stats_container.addWidget(
                StatCard("Avg Flowrate", f"{data.get('avg_flow') or 0:.2f}", "secondary"), 0, 1
            )
            self.stats_container.addWidget(
                StatCard("Avg Pressure", f"{data.get('avg_pressure') or 0:.2f}", "accent"), 0, 2
            )
            self.stats_container.addWidget(
                StatCard("Avg Temperature", f"{data.get('avg_temperature') or 0:.2f}", "success"), 0, 3
            )
        
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
        while self.charts_grid.count():
            item = self.charts_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Common matplotlib style
        plt.rcParams['text.color'] = COLORS['text_primary']
        plt.rcParams['axes.labelcolor'] = COLORS['text_secondary']
        plt.rcParams['xtick.color'] = COLORS['text_secondary']
        plt.rcParams['ytick.color'] = COLORS['text_secondary']
        plt.rcParams['axes.edgecolor'] = '#2a3f5f'  # Solid color instead of rgba
        plt.rcParams['grid.color'] = '#2a3f5f'
        plt.rcParams['grid.alpha'] = 0.3

        # --- Chart 1: Equipment Type Distribution (Vertical Bar) ---
        card1 = ChartCard("Equipment Distribution")
        fig1 = Figure(figsize=(5, 4), dpi=100, facecolor=COLORS['bg_card'])
        ax1 = fig1.add_subplot(111)
        ax1.set_facecolor(COLORS['bg_card'])
        
        if not df.empty and 'equipment_type' in df.columns:
            dist = df['equipment_type'].value_counts().sort_values(ascending=True)
            colors_bar = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
                         COLORS['success'], COLORS['warning'], '#a0aec0']
            
            bars = ax1.barh(range(len(dist)), dist.values, 
                           color=colors_bar[:len(dist)], alpha=0.8, height=0.6)
            
            ax1.set_yticks(range(len(dist)))
            ax1.set_yticklabels(dist.index, fontsize=10)
            ax1.set_xlabel('Count', fontsize=10, color=COLORS['text_secondary'])
            ax1.grid(axis='x', alpha=0.15, linestyle='--')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color('#2a3f5f')
            ax1.spines['bottom'].set_color('#2a3f5f')
            
            # Add value labels on bars
            for i, (bar, value) in enumerate(zip(bars, dist.values)):
                ax1.text(value + 0.5, i, str(value), 
                        va='center', fontsize=9, color=COLORS['text_primary'])
        
        fig1.tight_layout()
        canvas1 = FigureCanvasQTAgg(fig1)
        card1.set_chart(canvas1)
        self.charts_grid.addWidget(card1, 0, 0)

        # --- Chart 2: Avg Flowrate by Type (Horizontal Bar) ---
        card2 = ChartCard("Flowrate Analysis")
        fig2 = Figure(figsize=(5, 4), dpi=100, facecolor=COLORS['bg_card'])
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor(COLORS['bg_card'])

        if not df.empty and 'equipment_type' in df.columns and 'flowrate' in df.columns:
            df['flowrate'] = pd.to_numeric(df['flowrate'], errors='coerce')
            avg_flow_by_type = df.groupby('equipment_type')['flowrate'].mean().sort_values(ascending=True)
            
            bars = ax2.barh(range(len(avg_flow_by_type)), avg_flow_by_type.values, 
                           color=COLORS['secondary'], alpha=0.8, height=0.6)
            ax2.set_yticks(range(len(avg_flow_by_type)))
            ax2.set_yticklabels(avg_flow_by_type.index, fontsize=10)
            ax2.set_xlabel('Average Flowrate', fontsize=10, color=COLORS['text_secondary'])
            ax2.grid(axis='x', alpha=0.15, linestyle='--')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('#2a3f5f')
            ax2.spines['bottom'].set_color('#2a3f5f')
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, avg_flow_by_type.values)):
                ax2.text(value + 2, i, f'{value:.1f}', 
                        va='center', fontsize=9, color=COLORS['text_primary'])
        
        fig2.tight_layout()
        canvas2 = FigureCanvasQTAgg(fig2)
        card2.set_chart(canvas2)
        self.charts_grid.addWidget(card2, 0, 1)

        # --- Chart 3: Flow vs Pressure (Scatter) ---
        card3 = ChartCard("Correlation Analysis")
        fig3 = Figure(figsize=(5, 4), dpi=100, facecolor=COLORS['bg_card'])
        ax3 = fig3.add_subplot(111)
        ax3.set_facecolor(COLORS['bg_card'])

        if not df.empty and 'flowrate' in df.columns and 'pressure' in df.columns:
            df['flowrate'] = pd.to_numeric(df['flowrate'], errors='coerce')
            df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')
            
            ax3.scatter(df['flowrate'], df['pressure'], 
                       color=COLORS['accent'], alpha=0.6, s=50, edgecolors=COLORS['text_primary'], linewidth=0.5)
            ax3.set_xlabel('Flowrate', fontsize=10, color=COLORS['text_secondary'])
            ax3.set_ylabel('Pressure', fontsize=10, color=COLORS['text_secondary'])
            ax3.grid(True, alpha=0.2)
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
        
        fig3.tight_layout()
        canvas3 = FigureCanvasQTAgg(fig3)
        card3.set_chart(canvas3)
        self.charts_grid.addWidget(card3, 1, 0)
        
        # --- Chart 4: Temperature Distribution (Histogram) ---
        card4 = ChartCard("Temperature Distribution")
        fig4 = Figure(figsize=(5, 4), dpi=100, facecolor=COLORS['bg_card'])
        ax4 = fig4.add_subplot(111)
        ax4.set_facecolor(COLORS['bg_card'])

        if not df.empty and 'temperature' in df.columns:
            df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
            
            ax4.hist(df['temperature'].dropna(), bins=15, color=COLORS['success'], alpha=0.7, edgecolor=COLORS['text_primary'])
            ax4.set_xlabel('Temperature', fontsize=10, color=COLORS['text_secondary'])
            ax4.set_ylabel('Frequency', fontsize=10, color=COLORS['text_secondary'])
            ax4.grid(axis='y', alpha=0.2)
            ax4.spines['top'].set_visible(False)
            ax4.spines['right'].set_visible(False)
        
        fig4.tight_layout()
        canvas4 = FigureCanvasQTAgg(fig4)
        card4.set_chart(canvas4)
        self.charts_grid.addWidget(card4, 1, 1)

    def show_error(self, msg):
        err = QLabel(msg)
        err.setStyleSheet(f"color: {COLORS['accent']}; font-size: 14px; padding: 20px;")
        self.layout.addWidget(err)
