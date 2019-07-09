from page.edge_detection_page import EdgeDetectionPage

from tkinter import messagebox
import settings
import util as util


class BaselineController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl
        self.canvas = None
        self.refs = None

        self.test_item = None

    def connect_page(self, page):
        self.page = page
        self.canvas = page.canvas
        self.refs = {
            "image": self.page.canvas_image,
            "baseline": self.page.canvas_baseline,
            "drop_crop": self.page.canvas_drop_crop,
            "needle_crop": self.page.canvas_needle_crop
        }

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_move)

        self.page.next_button.config(command=self.send_images)
        self.page.reset_button.config(command=self.reset_lines)
    # end connect_page

    def before_hide(self):
        pass
    # end before_hide

    def before_show(self):
        self.test_item = self.main_ctrl.get_current_test()

        # show image first to get scale_factor
        self.show_image()

        # show lines and rects
        baseline = self.test_item.baseline
        drop_crop = self.test_item.drop_crop
        needle_crop = self.test_item.needle_crop
        scale_factor = self.test_item.scale_factor

        b1 = util.get_rescaled_baseline_coords(
            baseline.first_point, drop_crop, scale_factor
        )
        b2 = util.get_rescaled_baseline_coords(
            baseline.second_point, drop_crop, scale_factor
        )

        self.test_item.baseline_coords = [
            b1[0], b1[1], b2[0], b2[1]
        ]

        self.test_item.drop_crop_coords = util.get_rescaled_drop_coords(
            drop_crop, scale_factor
        )

        self.test_item.needle_crop_coords = util.get_rescaled_drop_coords(
            needle_crop, scale_factor
        )

        self.update_lines()
    # end before_show

    def update_data(self):
        self.before_show()

    def show_image(self):
        if(self.test_item.original_image is not None):
            # calculate scaling to get a fixed max width image
            if(self.test_item.original_image.size[0] > settings.STANDARD_IMAGE_WIDTH):
                self.test_item.scale_factor = settings.STANDARD_IMAGE_WIDTH / self.test_item.original_image.size[0]
            else:
                self.test_item.scale_factor = 1.0

            # calculate new size of canvas
            new_width = int(self.test_item.original_image.size[0] * self.test_item.scale_factor)
            new_height = int(self.test_item.original_image.size[1] * self.test_item.scale_factor)

            self.canvas.config(
                width=new_width,
                height=new_height
            )

            self.canvas.itemconfig(
                self.refs["image"],
                image=self.test_item.original_image_tk
            )
        else:
            self.canvas.config(
                width=1280,
                height=720
            )
            self.canvas.itemconfig(
                self.refs["image"],
                image=""
            )
        # end if image not None

    def handle_click(self, evt):
        pos = util.get_scaled_coords(evt, self.test_item.scale_factor)

        if(self.test_item.click_state == "needle_crop_1"):
            self.test_item.needle_crop = [pos["x"], pos["y"], pos["x"], pos["y"]]
            self.test_item.needle_crop_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.test_item.click_state = "needle_crop_2"
        elif(self.test_item.click_state == "needle_crop_2"):
            self.test_item.needle_crop[2] = pos["x"]
            self.test_item.needle_crop[3] = pos["y"]
            self.test_item.needle_crop_coords[2] = evt.x
            self.test_item.needle_crop_coords[3] = evt.y
            self.update_lines()
            # generate needle image
            self.generate_needle_image()
            self.test_item.click_state = "drop_crop_1"
        elif(self.test_item.click_state == "drop_crop_1"):
            self.test_item.drop_crop = [pos["x"], pos["y"], pos["x"], pos["y"]]
            self.test_item.drop_crop_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.test_item.click_state = "drop_crop_2"
        elif(self.test_item.click_state == "drop_crop_2"):
            self.test_item.drop_crop[2] = pos["x"]
            self.test_item.drop_crop[3] = pos["y"]
            self.test_item.drop_crop_coords[2] = evt.x
            self.test_item.drop_crop_coords[3] = evt.y
            self.update_lines()
            # generate drop image
            self.generate_drop_image()
            self.test_item.click_state = "baseline_1"
        elif(self.test_item.click_state == "baseline_1"):
            self.test_item.baseline.set_first_point(
                [
                    pos["x"] - self.test_item.drop_crop[0],
                    self.test_item.get_drop_crop_height() - (pos["y"] - self.test_item.drop_crop[1])
                ]
            )
            self.test_item.baseline.set_second_point(
                [
                    pos["x"] - self.test_item.drop_crop[0],
                    self.test_item.get_drop_crop_height() - (pos["y"] - self.test_item.drop_crop[1])
                ]
            )
            self.test_item.baseline_coords = [evt.x, evt.y, evt.x, evt.y]
            self.update_lines()
            self.test_item.click_state = "baseline_2"
        elif(self.test_item.click_state == "baseline_2"):
            self.test_item.baseline.set_second_point(
                [
                    pos["x"] - self.test_item.drop_crop[0],
                    self.test_item.get_drop_crop_height() - (pos["y"] - self.test_item.drop_crop[1])
                ]
            )
            self.test_item.baseline_coords[2] = evt.x
            self.test_item.baseline_coords[3] = evt.y
            # generate baseline
            self.test_item.baseline.calculate_params()
            self.update_lines()
            self.test_item.click_state = ""
    # end handle_click

    def handle_move(self, evt):
        if(self.test_item.click_state == "needle_crop_2"):
            self.test_item.needle_crop_coords[2] = evt.x
            self.test_item.needle_crop_coords[3] = evt.y
        elif(self.test_item.click_state == "drop_crop_2"):
            self.test_item.drop_crop_coords[2] = evt.x
            self.test_item.drop_crop_coords[3] = evt.y
        elif(self.test_item.click_state == "baseline_2"):
            self.test_item.baseline_coords[2] = evt.x
            self.test_item.baseline_coords[3] = evt.y

        self.update_lines()
    # end handle_move

    def update_lines(self):
        self.canvas.coords(
            self.refs["drop_crop"],
            (
                self.test_item.drop_crop_coords[0],
                self.test_item.drop_crop_coords[1],
                self.test_item.drop_crop_coords[2],
                self.test_item.drop_crop_coords[3],
            )
        )

        self.canvas.coords(
            self.refs["baseline"],
            (
                self.test_item.baseline_coords[0],
                self.test_item.baseline_coords[1],
                self.test_item.baseline_coords[2],
                self.test_item.baseline_coords[3],
            )
        )

        self.canvas.coords(
            self.refs["needle_crop"],
            (
                self.test_item.needle_crop_coords[0],
                self.test_item.needle_crop_coords[1],
                self.test_item.needle_crop_coords[2],
                self.test_item.needle_crop_coords[3]
            )
        )

        if(self.test_item.click_state == "needle_crop_1" or self.test_item.click_state == "needle_crop_2"):
            self.page.help_label.config(text="Nadelausschnitt setzen")
        elif(self.test_item.click_state == "drop_crop_1" or self.test_item.click_state == "drop_crop_2"):
            self.page.help_label.config(text="Tropfenausschnitt setzen")
        elif(self.test_item.click_state == "baseline_1" or self.test_item.click_state == "baseline_2"):
            self.page.help_label.config(text="Basisilinie setzen")
        else:
            self.page.help_label.config(text="Fertig")
    # end update_lines

    def reset_lines(self):
        self.test_item.baseline_coords = [0, 0, 0, 0]
        self.test_item.drop_crop_coords = [0, 0, 0, 0]
        self.test_item.needle_crop_coords = [0, 0, 0, 0]

        # values in respect to the original image
        self.test_item.drop_crop = [0, 0, 0, 0]
        self.test_item.needle_crop = [0, 0, 0, 0]
        self.test_item.baseline.reset_points()

        self.test_item.drop_image = None
        self.test_item.needle_image = None

        self.update_lines()
        self.test_item.click_state = "needle_crop_1"
    # end reset_lines

    def generate_needle_image(self):
        # needle crop
        dx = self.test_item.needle_crop[2] - self.test_item.needle_crop[0]
        dy = self.test_item.needle_crop[3] - self.test_item.needle_crop[1]

        if(dx != 0 and dy != 0):
            needle_image = self.test_item.original_image.crop(
                (
                    self.test_item.needle_crop[0],
                    self.test_item.needle_crop[1],
                    self.test_item.needle_crop[2],
                    self.test_item.needle_crop[3]
                )
            )
            needle_image = needle_image.convert("L")
            self.test_item.needle_image = needle_image
        else:
            messagebox.showinfo("Fehler", "Ungültiger Nadelausschnitt")
            self.test_item.needle_image = None
            return

    def generate_drop_image(self):
        dx = self.test_item.drop_crop[2] - self.test_item.drop_crop[0]
        dy = self.test_item.drop_crop[3] - self.test_item.drop_crop[1]

        if(dx != 0 and dy != 0):
            drop_image = self.test_item.original_image.crop(
                (
                    self.test_item.drop_crop[0],
                    self.test_item.drop_crop[1],
                    self.test_item.drop_crop[2],
                    self.test_item.drop_crop[3]
                )
            )
            drop_image = drop_image.convert("L")
            self.test_item.drop_image = drop_image
        else:
            messagebox.showinfo("Fehler", "Ungültiger Tropfenausschnitt")
            self.test_item.drop_image = None
            return

    def send_images(self):
        # check baseline
        if(self.test_item.baseline.is_finished() is not True):
            messagebox.showinfo("Fehler", "Ungültige Basislinie")
            return

        # send images
        if(self.test_item.needle_image is not None and self.test_item.drop_image is not None):
            self.main_ctrl.show_page(EdgeDetectionPage)
        else:
            messagebox.showinfo("Fehler", "Fehler beim Erzeugen der Bildausschnitte. Bitte prüfen, ob ein Bild geladen wurde.")
            return
    # end send_images
