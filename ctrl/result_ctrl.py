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

        fitting_points = self.main_ctrl.get_fitting_points()

        baseline_x = np.arange(0, drop_image_width, 1)
        left_x = np.arange(0, drop_image_width / 2, 1)
        right_x = np.arange(drop_image_width / 2, drop_image_width, 1)

        fit_result = self.main_ctrl.get_fit_result()
        print(fit_result)

        self.plot.cla()
        self.plot.scatter(
            points[:, 1],
            points[:, 0],
            marker=",",
            color="r",
            s=1
        )
        self.plot.scatter(
            fitting_points["left"][:, 1],
            fitting_points["left"][:, 0],
            marker=",",
            color="b",
            s=1
        )
        self.plot.scatter(
            fitting_points["right"][:, 1],
            fitting_points["right"][:, 0],
            marker=",",
            color="b",
            s=1
        )
        self.plot.plot(
            baseline_x,
            baseline.get_value(baseline_x)
        )
        self.plot.plot(
            left_x,
            fit_result["left_1d"](left_x),
            color="#00ffff"
        )
        self.plot.plot(
            right_x,
            fit_result["right_1d"](right_x),
            color="#00ffff"
        )
        self.plot.grid(
            True
        )
        self.plot.set_title("Tk Embed")
        self.plot.axis("scaled")

        self.canvas.draw()

    def update_label(self, label):
        label.config(text="Ich bin nur ein Test")
