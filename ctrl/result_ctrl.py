import numpy as np


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
        points = self.main_ctrl.get_edge_points()
        baseline = self.main_ctrl.get_baseline()
        drop_image_width = self.main_ctrl.get_drop_image().size[0]

        baseline_x = np.arange(0, drop_image_width, 1)

        self.plot.cla()
        self.plot.scatter(
            points[:, 1],
            points[:, 0],
            marker=",",
            color="r",
            s=1
        )
        self.plot.plot(
            baseline_x,
            baseline.get_value(baseline_x)
        )
        self.plot.set_title("Tk Embed")
        self.plot.axis("scaled")

        self.canvas.draw()

    def update_label(self, label):
        label.config(text="Ich bin nur ein Test")
