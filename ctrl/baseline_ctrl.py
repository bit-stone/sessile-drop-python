from PIL import ImageTk
from components.baseline import Baseline
from page.edge_detection_page import EdgeDetectionPage

IMAGE_WIDTH = 1280


class BaselineController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl
        self.canvas = None
        self.refs = None

        self.image = None
        self.image_tk = None
        self.scale_factor = 1.0

        self.click_state = "drop_crop_1"

        # positions in respect to scaled canvas
        # used to draw lines / rects
        self.baseline_coords = [0, 0, 0, 0]
        self.drop_crop_coords = [0, 0, 0, 0]
        self.needle_crop_coords = [0, 0, 0, 0]

        self.drop_crop = [0, 0, 0, 0]
        self.drop_crop_height = 0
        self.baseline = Baseline()

    def connect_page(self, page, canvas, canvas_refs):
        self.page = page
        self.canvas = canvas
        self.refs = canvas_refs

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_move)
    # end connect_page

    def before_hide(self):
        pass
    # end before_hide

    def before_show(self):
        self.image = self.main_ctrl.get_original_image()
        self.show_image()
    # end before_show

    def update_data(self):
        test = self.main_ctrl.get_current_test()
        # show image first to get scale_factor
        if(test.original_image is not None):
            self.image = test.original_image
        else:
            self.image = None
        self.show_image()

        # show lines and rects
        if(test.baseline is not None):
            self.baseline = test.baseline
            self.drop_crop = test.drop_crop

            b1 = self.get_rescaled_baseline_coords(
                self.baseline.first_point, self.drop_crop
            )
            b2 = self.get_rescaled_baseline_coords(
                self.baseline.second_point, self.drop_crop
            )

            self.baseline_coords = [
                b1[0], b1[1], b2[0], b2[1]
            ]

            self.drop_crop_coords = self.get_rescaled_drop_coords(
                self.drop_crop
            )

            self.update_lines()
        else:
            self.reset_lines()

    def show_image(self):
        if(self.image is not None):
            if(self.image.size[0] > IMAGE_WIDTH):
                self.scale_factor = IMAGE_WIDTH / self.image.size[0]
            else:
                self.scale_factor = 1.0

            print("Skalierung: ", self.scale_factor)

            new_width = int(self.image.size[0] * self.scale_factor)
            new_height = int(self.image.size[1] * self.scale_factor)

            self.image_tk = ImageTk.PhotoImage(
                image=self.image.resize((new_width, new_height))
            )

            self.canvas.config(
                width=new_width,
                height=new_height
            )

            self.canvas.itemconfig(
                self.refs["image"],
                image=self.image_tk
            )
        else:
            self.canvas.config(
                width=100,
                height=100
            )
            self.canvas.itemconfig(
                self.refs["image"],
                image=""
            )
        # end if image not None

    def handle_click(self, evt):
        pos = self.get_scaled_coords(evt)
        if(self.click_state == "drop_crop_1"):
            self.drop_crop = [pos["x"], pos["y"], pos["x"], pos["y"]]
            self.drop_crop_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.click_state = "drop_crop_2"
        elif(self.click_state == "drop_crop_2"):
            self.drop_crop[2] = pos["x"]
            self.drop_crop[3] = pos["y"]
            self.drop_crop_coords[2] = evt.x
            self.drop_crop_coords[3] = evt.y
            self.drop_crop_height = abs(
                int(self.drop_crop[3] - self.drop_crop[1])
            )
            self.update_lines()
            self.click_state = "baseline_1"
        elif(self.click_state == "baseline_1"):
            self.baseline.set_first_point(
                [
                    pos["x"] - self.drop_crop[0],
                    self.drop_crop_height - (pos["y"] - self.drop_crop[1])
                ]
            )
            self.baseline.set_second_point(
                [
                    pos["x"] - self.drop_crop[0],
                    self.drop_crop_height - (pos["y"] - self.drop_crop[1])
                ]
            )
            self.baseline_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.click_state = "baseline_2"
        elif(self.click_state == "baseline_2"):
            self.baseline.set_second_point(
                [
                    pos["x"] - self.drop_crop[0],
                    self.drop_crop_height - (pos["y"] - self.drop_crop[1])
                ]
            )
            self.baseline_coords[2] = evt.x
            self.baseline_coords[3] = evt.y
            self.baseline.calculate_params()
            self.update_lines()
            self.click_state = ""
    # end handle_click

    def handle_move(self, evt):
        if(self.click_state == "drop_crop_2"):
            self.drop_crop_coords[2] = evt.x
            self.drop_crop_coords[3] = evt.y
        elif(self.click_state == "baseline_2"):
            self.baseline_coords[2] = evt.x
            self.baseline_coords[3] = evt.y

        self.update_lines()
    # end handle_move

    def update_lines(self):
        self.canvas.coords(
            self.refs["drop_crop"],
            (
                self.drop_crop_coords[0],
                self.drop_crop_coords[1],
                self.drop_crop_coords[2],
                self.drop_crop_coords[3],
            )
        )

        self.canvas.coords(
            self.refs["baseline"],
            (
                self.baseline_coords[0],
                self.baseline_coords[1],
                self.baseline_coords[2],
                self.baseline_coords[3],
            )
        )
    # end update_lines

    def reset_lines(self):
        self.baseline_coords = [0, 0, 0, 0]
        self.drop_crop_coords = [0, 0, 0, 0]
        self.needle_crop_coords = [0, 0, 0, 0]

        # values in respect to the original image
        self.lines = {
            "baseline": [0, 0, 0, 0],
            "drop_crop": [0, 0, 0, 0],
            "needle_crop": [0, 0, 0, 0]
        }
        self.update_lines()
        self.click_state = "drop_crop_1"
    # end reset_lines

    def send_images(self):
        drop_image = None

        # apply crop
        dx = self.drop_crop[2] - self.drop_crop[0]
        dy = self.drop_crop[3] - self.drop_crop[1]

        if(dx != 0 and dy != 0):
            drop_image = self.image.crop(
                (
                    self.drop_crop[0],
                    self.drop_crop[1],
                    self.drop_crop[2],
                    self.drop_crop[3]
                )
            )
            drop_image = drop_image.convert("L")

        if(drop_image is not None):
            self.main_ctrl.set_drop_image(drop_image)
            self.main_ctrl.set_drop_crop(self.drop_crop)
            self.main_ctrl.set_baseline(self.baseline)
            self.main_ctrl.show_page(EdgeDetectionPage)

    # end send_images

    def get_scaled_coords(self, evt):
        mx = int(evt.x * ((1.0) / self.scale_factor))
        my = int(evt.y * ((1.0) / self.scale_factor))
        return {"x": mx, "y": my}
    # end get_scaled_coords

    def get_rescaled_baseline_coords(self, point, drop_crop):
        dch = drop_crop[3] - drop_crop[1]
        return (
            int((point[0] + drop_crop[0]) * self.scale_factor),
            int(((dch - point[1]) + drop_crop[1]) * self.scale_factor)
        )
    # end get_rescaled_baseline_coords

    def get_rescaled_drop_coords(self, drop_crop):
        return [
            int(drop_crop[0] * self.scale_factor),
            int(drop_crop[1] * self.scale_factor),
            int(drop_crop[2] * self.scale_factor),
            int(drop_crop[3] * self.scale_factor)
        ]
    # end get_rescaled_drop_coords
