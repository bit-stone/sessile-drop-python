import tkinter as tk


class StartPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        label = tk.Label(self, text="Start Page")
        label.grid(row=0, column=0)

        button = tk.Button(
            self,
            text="Go To Image Input",
            command=lambda: self.ctrl.show_image_input()
        )
        button.grid(row=1, column=0)

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()
