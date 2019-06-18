import tkinter as tk


class FittingPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        needle_label = tk.Label(self, text="Nadel Parameter: ")
        needle_label.grid(row=0, column=0)

        self.needle_width_label = tk.Label(self, text="")
        self.needle_width_label.grid(row=1, column=0)

        self.needle_angle_label = tk.Label(self, text="")
        self.needle_angle_label.grid(row=2, column=0)

        label = tk.Label(
            self,
            text="Fitting-Parameter und Methode"
        )
        label.grid(row=9, column=0, pady=(50, 5))

        self.method_var = tk.StringVar(self)
        self.method_var.set("tangent_1")

        self.method_selection = tk.OptionMenu(
            self,
            self.method_var,
            "tangent_1",
            "circle",
            "tangent_2",
            command=self.ctrl.update_fitting_method
        )
        self.method_selection.grid(row=10, column=0)

        next_button = tk.Button(
            self,
            text="Fitting durchführen",
            command=self.ctrl.request_fitting
        )
        next_button.grid(row=11, column=0)

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        self.ctrl.update_data()
