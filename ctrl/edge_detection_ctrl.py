from PIL import Image, ImageTk

from components.edge_detection import EdgeDetection

class EdgeDetectionController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl

        self.edge_detection = EdgeDetection()

        self.input_image = None

        self.drop_image = None
        self.drop_tk_image = None

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
            self.drop_tk_image = ImageTk.PhotoImage(
                image=image.resize((500, 282))
            )
            self.output_widget.configure(
                image=self.drop_tk_image
            )

    def request_edge_detection(self):
        if(self.input_image is not None):
            method = self.page.method_var.get()
            result = None
            if(method == "sobel_canny"):
                result = self.edge_detection.sobel_canny(
                    self.input_image,
                    self.page.top_scale.get(),
                    self.page.bottom_scale.get()
                )
            elif(method == "bw_threshold_linear"):
                result = self.edge_detection.bw_threshold_linear(
                    self.input_image,
                    self.page.top_scale.get()
                )

            if(result is not None):
                self.drop_image = Image.fromarray(result, mode="L")
                self.draw_output_image(self.drop_image)
    # end request_edge_detection
