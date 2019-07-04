import tkinter as tk


class BaselinePage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        label = tk.Label(
            self,
            text="Zuschnitt und Basislinie",
            font=("", 15)
        )
        label.grid(row=0, column=0)

        self.canvas = tk.Canvas(self, width=500, height=282, cursor='cross')
        self.canvas.grid(row=10, column=0)

        self.canvas_image = self.canvas.create_image((0, 0), anchor="nw")
        self.canvas_baseline = self.canvas.create_line(
            (0, 0, 0, 0), fill="red"
        )
        self.canvas_drop_crop = self.canvas.create_rectangle(
            (0, 0, 0, 0), outline="yellow"
        )
        self.canvas_needle_crop = self.canvas.create_rectangle(
            (0, 0, 0, 0), outline="green"
        )

        self.help_label = tk.Label(self, text="Start")
        self.help_label.grid(row=20, column=0)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=30, column=0)

        self.reset_button = tk.Button(
            self.button_frame,
            text="Erneut zuschneiden"
        )
        self.reset_button.grid(row=0, column=0)

        self.next_button = tk.Button(
            self.button_frame,
            text="Übernehmen"
        )
        self.next_button.grid(row=0, column=1)

        self.ctrl.connect_page(self)
    # end __init__

    def before_hide(self):
        self.ctrl.before_hide()
    # end before_hide

    def before_show(self):
        self.ctrl.before_show()
    # end before_show

    def update_data(self):
        self.ctrl.update_data()
