from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")


class ResultPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas._tkcanvas.grid(row=1, column=0)

        label = tk.Label(self, text="Ergebnisse")
        label.grid(row=0, column=0)

        label_frame = tk.Frame(self)
        label_frame.grid(row=2, column=0)

        self.left_angle_label = tk.Label(label_frame, text="Winkel links: 0°")
        self.left_angle_label.grid(row=0, column=0)

        self.avg_angle_label = tk.Label(label_frame, text="Mittlerer Winkel: 0°")
        self.avg_angle_label.grid(row=0, column=1)

        self.right_angle_label = tk.Label(label_frame, text="Rechter Winkel: 0°")
        self.right_angle_label.grid(row=0, column=2)

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        self.ctrl.update_data()
