from PIL import Image

import settings
from tkinter import messagebox
import util as util

from components.edge_detection import EdgeDetection

from page.fitting_page import FittingPage


class EdgeDetectionController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl

        self.test_item = None

        self.edge_detection = EdgeDetection()

    # end __init__

    def connect_page(self, page):
        self.page = page
        self.output_widget = page.output_widget

        self.page.send_data_button.config(command=self.next_command)
        self.page.test_button.config(command=self.request_edge_detection)

        self.page.top_scale.config(command=self.update_top_scale)
        self.page.bottom_scale.config(command=self.update_bottom_scale)
    # end connect_page

    def before_hide(self):
        pass
    # end before_hide

    def before_show(self):
        self.test_item = self.main_ctrl.get_current_test()

        self.page.method_var.set(self.test_item.edge_method)
        self.page.top_scale.set(self.test_item.edge_value_top)
        self.page.bottom_scale.set(self.test_item.edge_value_bottom)
        self.update_scales()

        if(self.test_item.drop_image is not None
           and self.test_item.needle_image is not None):
            self.request_edge_detection()
        else:
            self.output_widget.configure(image="")
    # end before_show

    def update_data(self):
        self.before_show()

    def update_detection_method(self, value):
        self.test_item.edge_method = self.page.method_var.get()
        if(self.test_item.edge_method == "sobel_canny"):
            self.page.top_scale.set(settings.SOBEL_DEFAULT_TOP)
            self.test_item.edge_value_top = settings.SOBEL_DEFAULT_TOP
            self.page.bottom_scale.set(settings.SOBEL_DEFAULT_BOTTOM)
            self.test_item.edge_value_bottom = settings.SOBEL_DEFAULT_BOTTOM
        elif(self.test_item.edge_method == "bw_threshold_linear"):
            self.page.top_scale.set(settings.BW_DEFAULT_THRESHOLD)
            self.test_item.edge_value_top = settings.BW_DEFAULT_THRESHOLD
        self.update_scales()
    # end update_detection_method

    def update_top_scale(self, value):
        self.test_item.edge_value_top = int(value)

    def update_bottom_scale(self, value):
        self.test_item.edge_value_bottom = int(value)

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

    def request_edge_detection(self):
        # detect needle
        if(self.test_item.needle_image is not None):
            needle_data = self.edge_detection.needle_detection(
                self.test_item.needle_image
            )
            self.test_item.needle_pixel_width = needle_data["width"]
            self.test_item.needle_angle = needle_data["angle"]

        # detect drop
        if(self.test_item.drop_image is not None):
            drop_data = None
            if(self.test_item.edge_method == "sobel_canny"):
                drop_data = self.edge_detection.sobel_canny(
                    self.test_item.drop_image,
                    self.test_item.edge_value_top,
                    self.test_item.edge_value_bottom
                )
            elif(self.test_item.edge_method == "bw_threshold_linear"):
                drop_data = self.edge_detection.bw_threshold_linear(
                    self.test_item.drop_image,
                    self.test_item.edge_value_top
                )

            if(drop_data is not None):
                self.test_item.edge_points = drop_data["points"]

                self.test_item.edge_image = Image.fromarray(
                    drop_data["image"],
                    mode="L"
                )
                self.test_item.edge_image_tk = util.image_to_widget(
                    self.test_item.edge_image, self.output_widget
                )
    # end request_edge_detection

    def next_command(self):
        if(len(self.test_item.edge_points) > 0):
            self.main_ctrl.show_page(FittingPage)
        else:
            messagebox.showinfo("Fehler", "Kantenerkennung produziert kein oder ein leeres Ergebnis")
