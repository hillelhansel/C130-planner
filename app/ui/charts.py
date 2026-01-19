# app/ui/charts.py
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class ChartsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        
        # INCREASED HEIGHT: 5.0 inches
        self.fig = Figure(figsize=(12, 5.0), dpi=100)
        self.fig.patch.set_facecolor('#2b2b2b')
        self.fig.subplots_adjust(bottom=0.15, top=0.9, left=0.08, right=0.95, wspace=0.25)
        
        # --- Chart 1: Weight vs %MAC ---
        self.ax1 = self.fig.add_subplot(121)
        
        # שינוי טווח ל-14 עד 32
        # [xmin, xmax, ymin, ymax]
        self.load_background_chart(self.ax1, "assets/chart_mac.png", [14, 32, 80000, 175000])
        self.format_ax(self.ax1, "Weight vs %MAC", [14, 32], [80000, 175000])
        
        self.dot1, = self.ax1.plot([], [], 'ro', markersize=12, markeredgecolor='black', label='Current')
        
        # --- Chart 2: Fuel vs ZFW ---
        self.ax2 = self.fig.add_subplot(122)
        # Fuel range 0-70000
        self.load_background_chart(self.ax2, "assets/chart_fuel.png", [0, 70000, 80000, 170000])
        self.format_ax(self.ax2, "Fuel vs ZFW", [0, 70000], [80000, 170000])
        self.dot2, = self.ax2.plot([], [], 'ro', markersize=12, markeredgecolor='black')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_background_chart(self, ax, path, extent):
        if os.path.exists(path):
            try:
                img = mpimg.imread(path)
                ax.imshow(img, extent=extent, aspect='auto', zorder=0)
            except Exception as e:
                print(f"Error loading chart: {e}")

    def format_ax(self, ax, title, xlim, ylim):
        ax.set_title(title, color='white', fontsize=11, weight='bold')
        ax.tick_params(colors='white', labelsize=9)
        ax.set_facecolor('none') 
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(1)

    def update_data(self, gw, zfw, fuel, mac):
        self.dot1.set_data([mac], [gw])
        self.dot2.set_data([fuel], [zfw])
        self.canvas.draw()