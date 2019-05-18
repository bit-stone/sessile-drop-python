import tkinter as tk


class Toolbar(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        start_page_button = tk.Button(
            self,
            text="Start",
            command=lambda: self.ctrl.show_page("start")
        )
        start_page_button.grid(row=0, column=0, sticky="nw")

        image_input_button = tk.Button(
            self,
            text="Bildeingabe",
            command=lambda: self.ctrl.show_page("image_input")
        )
        image_input_button.grid(row=0, column=1, sticky="nw")

        baseline_button = tk.Button(
            self,
            text="Baseline",
            command=lambda: self.ctrl.show_page("baseline")
        )
        baseline_button.grid(row=0, column=2, sticky="nw")

        fitting_button = tk.Button(
            self,
            text="Fitting",
            command=lambda: self.ctrl.show_page("fitting")
        )
        fitting_button.grid(row=0, column=3)

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()
