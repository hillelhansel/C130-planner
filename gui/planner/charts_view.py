import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import os

class ChartsView(ctk.CTkFrame):
    def __init__(self, parent, mgr):
        super().__init__(parent, corner_radius=0, fg_color="#2b2b2b")
        self.mgr = mgr
        
        # הגדרת הגודל והרקע
        self.fig = Figure(figsize=(12, 5.0), dpi=100)
        self.fig.patch.set_facecolor('#2b2b2b')
        self.fig.subplots_adjust(bottom=0.15, top=0.9, left=0.08, right=0.95, wspace=0.25)
        
        # --- Chart 1: Weight vs %MAC ---
        self.ax1 = self.fig.add_subplot(121)
        self.load_background_chart(self.ax1, "assets/chart_mac.png", [14, 32, 80000, 175000])
        self.format_ax(self.ax1, "Weight vs %MAC", [14, 32], [80000, 175000])
        self.dot1, = self.ax1.plot([], [], 'ro', markersize=12, markeredgecolor='black', label='Current')
        
        # --- Chart 2: Fuel vs ZFW ---
        self.ax2 = self.fig.add_subplot(122)
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
                print(f"Chart BG Error: {e}")

    def format_ax(self, ax, title, xlim, ylim):
        ax.set_title(title, color='white', fontsize=11, weight='bold')
        ax.tick_params(colors='white', labelsize=9)
        ax.set_facecolor('none') 
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(1)

    def update_view(self, data):
        # חילוץ הנתונים מהמילון data והעברתם לגרפים
        gw = data.get('gw', 0)
        zfw = data.get('zfw', 0)
        fuel = data.get('fuel_w', 0)
        mac = data.get('mac', 0)
        
        self.dot1.set_data([mac], [gw])
        self.dot2.set_data([fuel], [zfw])
        self.canvas.draw()