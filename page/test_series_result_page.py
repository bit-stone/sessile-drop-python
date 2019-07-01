import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib
matplotlib.use("TkAgg")


class TestSeriesResultPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas._tkcanvas.grid(row=1, column=0)

        self.label_frame = tk.Frame(self)
        self.label_frame.grid(row=2, column=0)

        self.line_label = tk.Label(self.label_frame, text="")
        self.line_label.grid(row=0, column=0)

        self.result_label = tk.Label(self.label_frame, text="")
        self.result_label.grid(row=1, column=0)

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        pass
