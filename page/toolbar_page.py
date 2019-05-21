import tkinter as tk


class ToolbarPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

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

        edge_button = tk.Button(
            self,
            text="Kantenerkennung",
            command=lambda: self.ctrl.show_page("edge_detection")
        )
        edge_button.grid(row=0, column=3, sticky="nw")

        fitting_button = tk.Button(
            self,
            text="Fitting",
            command=lambda: self.ctrl.show_page("fitting")
        )
        fitting_button.grid(row=0, column=4)

        result_page_button = tk.Button(
            self,
            text="Ergebnis",
            command=lambda: self.ctrl.show_page("result")
        )
        result_page_button.grid(row=0, column=5, sticky="nw")

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()
