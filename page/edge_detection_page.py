import tkinter as tk


class EdgeDetectionPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        label = tk.Label(
            self,
            text="Kantenerkennung Methode und Vorschau"
        )
        label.grid(row=0, column=0)

        self.ctrl.connect_page(self)
    # end __init__

    def before_hide(self):
        self.ctrl.before_hide()
    # end before_hide

    def before_show(self):
        self.ctrl.before_show()
    # end before_show
