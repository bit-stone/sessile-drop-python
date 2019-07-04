from PIL import Image, ImageTk
import numpy as np
import math
import numpy.linalg as npla
import settings
from tkinter import messagebox

from components.edge_detection import EdgeDetection

from page.fitting_page import FittingPage


class EdgeDetectionController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl

        self.edge_detection = EdgeDetection()

        self.input_image = None

        self.drop_image = None
        self.drop_tk_image = None

        self.needle_image = None
        self.needle_tk_image = None

        self.result = None
        self.needle_data = None

    # end __init__

    def connect_page(self, page):
        self.page = page
        self.output_widget = page.output_widget

        self.page.send_data_button.config(command=self.send_data)
        self.page.test_button.config(command=self.request_edge_detection)

        # does not work :(
        # self.page.method_selection.config(command=self.update_detection_method)
    # end connect_page

    def before_hide(self):
        pass
    # end before_hide

    def before_show(self):
        test = self.main_ctrl.get_current_test()

        params = test.edge_params
        if(params is not None):
            # set params
            self.page.method_var.set(params["method"])
            self.page.top_scale.set(params["top"])
            self.page.bottom_scale.set(params["bottom"])
            self.update_scales()

        self.input_drop_image = test.drop_image
        self.input_needle_image = test.needle_image

        if(self.input_drop_image is not None
           and self.input_needle_image is not None):
            self.request_edge_detection()
        else:
            self.output_widget.configure(image="")
    # end before_show

    def update_data(self):
        self.before_show()

    def update_detection_method(self, value):
        method = self.page.method_var.get()
        if(method == "sobel_canny"):
            self.page.top_scale.set(settings.SOBEL_DEFAULT_TOP)
            self.page.bottom_scale.set(settings.SOBEL_DEFAULT_BOTTOM)
        elif(method == "bw_threshold_linear"):
            self.page.top_scale.set(settings.BW_DEFAULT_THRESHOLD)
        self.update_scales()
    # end update_detection_method

    def update_scales(self):
        method = self.page.method_var.get()
        if(method == "sobel_canny"):
            # show both scales, labeled top/bottom
            self.page.top_scale.config(
                label="Top"
            )
            self.page.bottom_scale.config(
                label="Bottom"
            )
            self.page.bottom_scale.grid()
        elif(method == "bw_threshold_linear"):
            # show only left scale, labeled threshold
            self.page.top_scale.config(
                label="Threshold"
            )
            self.page.bottom_scale.grid_remove()
    # end update_scales

    def draw_output_image(self, image):
        if(image is not None):
            scale_factor = 1.0
            if(image.size[0] > settings.STANDARD_IMAGE_WIDTH):
                scale_factor = settings.STANDARD_IMAGE_WIDTH / image.size[0]

            width = int(image.size[0] * scale_factor)
            height = int(image.size[1] * scale_factor)
            self.drop_tk_image = ImageTk.PhotoImage(
                image=image.resize((width, height))
            )
            self.output_widget.configure(
                image=self.drop_tk_image
            )
    # end draw_output_image

    def request_edge_detection(self):
        # detect needle
        if(self.input_needle_image is not None):
            self.needle_data = None

            self.needle_result = self.edge_detection.sobel_canny(
                self.input_needle_image,
                settings.SOBEL_NEEDLE_TOP,
                settings.SOBEL_NEEDLE_BOTTOM
            )

            # get middle point
            needle_left = np.amin(self.needle_result["points"], axis=0)[1]
            needle_right = np.amax(self.needle_result["points"], axis=0)[1]
            needle_middle_point = needle_right - needle_left

            # filter points to left/right
            left_needle_points = self.needle_result["points"][
                self.needle_result["points"][:,1] <= needle_middle_point
            ]

            right_needle_points = self.needle_result["points"][
                self.needle_result["points"][:,1] > needle_middle_point
            ]

            # reduce left/right to one average value to get distance
            needle_avg_left = np.average(left_needle_points[:,1])
            needle_avg_right = np.average(right_needle_points[:,1])

            needle_width = needle_avg_right - needle_avg_left

            # get angle and apply it to before mentioned distance
            # first fit line to left/right
            needle_left_fit = np.polyfit(
                left_needle_points[:,0],
                left_needle_points[:,1],
                1
            )

            needle_right_fit = np.polyfit(
                right_needle_points[:,0],
                right_needle_points[:,1],
                1
            )

            avg_m = (needle_left_fit[0] + needle_right_fit[0]) / 2.0

            needle_angle = self.calculate_angle(
                [1, 0],
                [1, avg_m]
            )

            needle_width = needle_width * math.cos(needle_angle)

            self.needle_data = {
                "width": needle_width,
                "angle": needle_angle,
                "angle_degrees": math.degrees(needle_angle)
            }

        # detect drop
        if(self.input_drop_image is not None):
            method = self.page.method_var.get()
            self.result = None
            if(method == "sobel_canny"):
                self.result = self.edge_detection.sobel_canny(
                    self.input_drop_image,
                    self.page.top_scale.get(),
                    self.page.bottom_scale.get()
                )
            elif(method == "bw_threshold_linear"):
                self.result = self.edge_detection.bw_threshold_linear(
                    self.input_drop_image,
                    self.page.top_scale.get()
                )

            if(self.result is not None):
                self.drop_image = Image.fromarray(
                    self.result["image"],
                    mode="L"
                )
                self.draw_output_image(self.drop_image)
    # end request_edge_detection

    def send_data(self):
        if(self.result is not None and self.result["points"] is not None):
            self.main_ctrl.set_edge_points(self.result["points"])
            self.main_ctrl.set_needle_data(self.needle_data)
            self.main_ctrl.set_edge_params({
                "method": self.page.method_var.get(),
                "top": self.page.top_scale.get(),
                "bottom": self.page.bottom_scale.get()
            })
            self.main_ctrl.show_page(FittingPage)
        else:
            messagebox.showinfo("Fehler", "Kantenerkennung produziert kein Ergebnis")

    def calculate_angle(self, vec_1, vec_2):
        result = np.dot(vec_1, vec_2) / (
            (npla.norm(vec_1)) * (npla.norm(vec_2))
        )
        result = math.acos(result)

        return result
