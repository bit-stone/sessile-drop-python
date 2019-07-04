import tkinter as tk


class ToolbarPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        self.image_input_button = tk.Button(
            self,
            text="Bildeingabe"
        )
        self.image_input_button.grid(row=0, column=1, sticky="nw")

        self.baseline_button = tk.Button(
            self,
            text="Baseline"
        )
        self.baseline_button.grid(row=0, column=2, sticky="nw")

        self.edge_button = tk.Button(
            self,
            text="Kantenerkennung"
        )
        self.edge_button.grid(row=0, column=3, sticky="nw")

        self.fitting_button = tk.Button(
            self,
            text="Fitting"
        )
        self.fitting_button.grid(row=0, column=4)

        self.result_page_button = tk.Button(
            self,
            text="Ergebnis"
        )
        self.result_page_button.grid(row=0, column=5, sticky="nw")

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        pass
