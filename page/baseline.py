import tkinter as tk


class BaselinePage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        self.canvas = tk.Canvas(self, width=500, height=282)
        self.canvas.grid(row=0, column=0)

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

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0)

        self.ctrl.connect_page(
            self,
            self.canvas,
            {
                "image": self.canvas_image,
                "baseline": self.canvas_baseline,
                "drop_crop": self.canvas_drop_crop,
                "needle_crop": self.canvas_needle_crop
            }
        )
    # end __init__

    def before_hide(self):
        self.ctrl.before_hide()
    # end before_hide

    def before_show(self):
        self.ctrl.before_show()
    # end before_show
