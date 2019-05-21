from PIL import ImageTk

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

        # values in respect to the original image
        self.lines = {
            "baseline": [0, 0, 0, 0],
            "drop_crop": [0, 0, 0, 0],
            "needle_crop": [0, 0, 0, 0]
        }

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
        if(self.image is not None):
            if(self.image.size[0] > IMAGE_WIDTH):
                self.scale_factor = IMAGE_WIDTH / self.image.size[0]
            else:
                self.scale_factor = 1.0

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
        # end if image not None
    # end before_show

    def handle_click(self, evt):
        pos = self.get_scaled_coords(evt)
        print(self.click_state)
        if(self.click_state == "drop_crop_1"):
            self.lines["drop_crop"] = [pos["x"], pos["y"], pos["x"], pos["y"]]
            self.drop_crop_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.click_state = "drop_crop_2"
        elif(self.click_state == "drop_crop_2"):
            self.lines["drop_crop"][2] = pos["x"]
            self.lines["drop_crop"][3] = pos["y"]
            self.drop_crop_coords[2] = evt.x
            self.drop_crop_coords[3] = evt.y
            self.update_lines()
            self.click_state = "baseline_1"
        elif(self.click_state == "baseline_1"):
            self.lines["baseline"] = [pos["x"], pos["y"], pos["x"], pos["y"]]
            self.baseline_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.click_state = "baseline_2"
        elif(self.click_state == "baseline_2"):
            self.lines["baseline"][2] = pos["x"]
            self.lines["baseline"][3] = pos["y"]
            self.baseline_coords[2] = evt.x
            self.baseline_coords[3] = evt.y
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
        dx = self.lines["drop_crop"][2] - self.lines["drop_crop"][0]
        dy = self.lines["drop_crop"][3] - self.lines["drop_crop"][1]

        if(dx != 0 and dy != 0):
            drop_image = self.image.crop(
                (
                    self.lines["drop_crop"][0],
                    self.lines["drop_crop"][1],
                    self.lines["drop_crop"][2],
                    self.lines["drop_crop"][3]
                )
            )
            drop_image = drop_image.convert("L")

        if(drop_image is not None):
            drop_image.show()

    # end send_images

    def get_scaled_coords(self, evt):
        mx = int(evt.x * ((1.0) / self.scale_factor))
        my = int(evt.y * ((1.0) / self.scale_factor))
        return {"x": mx, "y": my}
    # end get_scaled_coords
