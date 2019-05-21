from numpy import arange, sin, pi


class ResultController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl
        self.plot = None
        self.canvas = None
        self.count = 0

    def connect_page(self, page, canvas, plot):
        self.page = page
        self.canvas = canvas
        self.plot = plot

    def before_hide(self):
        pass

    def before_show(self):
        self.count += 0.1
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t) * self.count

        self.plot.cla()
        self.plot.plot(t, s)
        self.plot.set_title("Tk Embed")

        self.canvas.draw()

    def update_label(self, label):
        label.config(text="Ich bin nur ein Test")
