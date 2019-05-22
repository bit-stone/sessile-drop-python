from PIL import Image, ImageTk
import settings

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

        self.result = None

    # end __init__

    def connect_page(self, page):
        self.page = page
        self.output_widget = page.output_widget
    # end connect_page

    def before_hide(self):
        pass
    # end before_hide

    def before_show(self):
        self.update_scales("")
        self.input_image = self.main_ctrl.get_drop_image()
        self.draw_output_image(self.input_image)
    # end before_show

    def update_scales(self, value):
        method = self.page.method_var.get()
        if(method == "sobel_canny"):
            # show both scales, labeled top/bottom
            self.page.top_scale.config(
                label="Top"
            )
            self.page.top_scale.set(settings.SOBEL_DEFAULT_TOP)
            self.page.bottom_scale.config(
                label="Bottom"
            )
            self.page.bottom_scale.set(settings.SOBEL_DEFAULT_BOTTOM)
            self.page.bottom_scale.grid()
        elif(method == "bw_threshold_linear"):
            # show only left scale, labeled threshold
            self.page.top_scale.config(
                label="Threshold"
            )
            self.page.top_scale.set(settings.BW_DEFAULT_THRESHOLD)
            self.page.bottom_scale.grid_remove()
    # end update_scales

    def draw_output_image(self, image):
        if(image is not None):
            scale_factor = 1.0
            if(image.size[0] > 500):
                scale_factor = 500 / image.size[0]

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
        if(self.input_image is not None):
            method = self.page.method_var.get()
            self.result = None
            if(method == "sobel_canny"):
                self.result = self.edge_detection.sobel_canny(
                    self.input_image,
                    self.page.top_scale.get(),
                    self.page.bottom_scale.get()
                )
            elif(method == "bw_threshold_linear"):
                self.result = self.edge_detection.bw_threshold_linear(
                    self.input_image,
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
        if(self.result["points"] is not None):
            self.main_ctrl.set_edge_points(self.result["points"])
            self.main_ctrl.show_page(FittingPage)
