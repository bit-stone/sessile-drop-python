import numpy as np
import math

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
        self.show_result_data()

    def update_data(self):
        self.show_result_data()

    def show_result_data(self):
        test = self.main_ctrl.get_current_test()

        if(test.drop_image is not None and test.fit_result is not None):
            point_list = test.drop_edge_points
            baseline = test.baseline
            drop_image_width = test.drop_image.size[0]

            fitting_points = {
                "left": test.left_points,
                "right": test.right_points
            }

            baseline_x = np.arange(0, drop_image_width, 1)
            left_x = np.arange(0, drop_image_width / 2, 1)
            right_x = np.arange(drop_image_width / 2, drop_image_width, 1)

            fit_result = test.fit_result

            self.plot.cla()
            self.plot.scatter(
                point_list[:, 1],
                point_list[:, 0],
                marker=",",
                color="r",
                s=1
            )
            self.plot.scatter(
                fitting_points["left"][:, 1],
                fitting_points["left"][:, 0],
                marker=",",
                color="y",
                s=1
            )
            self.plot.scatter(
                fitting_points["right"][:, 1],
                fitting_points["right"][:, 0],
                marker=",",
                color="y",
                s=1
            )
            self.plot.plot(
                baseline_x,
                baseline.get_value(baseline_x)
            )

            vl = [50, baseline.m * 50]
            vr = [-50, -baseline.m * 50]
            la = fit_result["left_angle"]
            ra = fit_result["right_angle"]

            # turn anti clockwise
            left_vec = [
                math.cos(-la) * vl[0] + math.sin(-la) * vl[1],
                -math.sin(-la) * vl[0] + math.cos(-la) * vl[1]
            ]

            # turn clockwise
            right_vec = [
                math.cos(ra) * vr[0] + math.sin(ra) * vr[1],
                -math.sin(ra) * vr[0] + math.cos(ra) * vr[1]
            ]

            # draw angles
            X = [
                fit_result["left_contact_point"][1],
                fit_result["right_contact_point"][1]
            ]

            Y = [
                fit_result["left_contact_point"][0],
                fit_result["right_contact_point"][0]
            ]

            U = [
                left_vec[0],
                right_vec[0]
            ]

            V = [
                left_vec[1],
                right_vec[1]
            ]

            self.plot.quiver(
                X, Y, U, V, angles="xy", scale_units="xy", scale=1, width=0.004, color="b"
            )

            if(fit_result["flipped"]):
                # self.plot.plot(
                #     fit_result["left_1d"](left_x),
                #     left_x,
                #     color="g"
                # )
                # self.plot.plot(
                #     fit_result["right_1d"](right_x),
                #     right_x,
                #     color="y"
                # )
                pass
            else:
                # self.plot.plot(
                #     left_x,
                #     fit_result["left_1d"](left_x),
                #     color="g"
                # )
                # self.plot.plot(
                #     right_x,
                #     fit_result["right_1d"](right_x),
                #     color="y"
                # )
                pass

            self.plot.grid(
                True
            )
            self.plot.set_title("Tk Embed")
            self.plot.axis("scaled")

            self.canvas.draw()

            self.page.left_angle_label.config(text="Linker Winkel: {0:.2f}°".format(math.degrees(fit_result["left_angle"])))
            self.page.right_angle_label.config(text="Rechter Winkel: {0:.2f}°".format(math.degrees(fit_result["right_angle"])))

            avg_angle = (fit_result["left_angle"] + fit_result["right_angle"]) / 2.0
            self.page.avg_angle_label.config(text="Mittlerer Winkel: {0:.2f}°".format(math.degrees(avg_angle)))
