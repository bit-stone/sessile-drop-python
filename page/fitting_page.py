import tkinter as tk


class FittingPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        needle_label = tk.Label(self, text="Erkannte Nadel-Parameter: ")
        needle_label.grid(row=0, column=0)

        self.needle_width_label = tk.Label(self, text="")
        self.needle_width_label.grid(row=1, column=0)

        self.needle_angle_label = tk.Label(self, text="")
        self.needle_angle_label.grid(row=2, column=0)

        fluid_label = tk.Label(
            self,
            text="Verwendete Flüssigkeit:"
        )
        fluid_label.grid(row=7, column=0, pady=(50, 5))

        self.fluid_var = tk.StringVar(self)
        self.fluid_var.set("")

        label = tk.Label(
            self,
            text="Fitting-Methode:"
        )
        label.grid(row=9, column=0, pady=(50, 5))

        # fluid option menu created in connect_page

        self.method_var = tk.StringVar(self)
        self.method_var.set("tangent_1")

        # OptionMenu needs to have its command when created
        self.method_selection = tk.OptionMenu(
            self,
            self.method_var,
            "tangent_1",
            "circle",
            "tangent_2",
            command=self.ctrl.update_fitting_method
        )
        self.method_selection.grid(row=10, column=0)

        self.request_fitting_button = tk.Button(
            self,
            text="Fitting durchführen"
        )
        self.request_fitting_button.grid(row=11, column=0)

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        self.ctrl.update_data()
