import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import settings

from page.baseline_page import BaselinePage


class ImageInputController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl

        self.camera = None
        self.camera_running = False

        self.output_widget = None
        self.start_camera_button = None

        self.image = None
        self.image_tk = None

    def connect_page(self, page, output_widget, start_camera_button):
        self.page = page
        self.output_widget = output_widget
        self.start_camera_button = start_camera_button
        self.init_image_input()

    def before_hide(self):
        self.pause_camera()

    def before_show(self):
        if(self.camera is not None and self.camera.isOpened() is not True):
            self.init_image_input()

        test = self.main_ctrl.get_current_test()
        self.image = test.original_image
        # print(self.image)
        if(self.image is not None):
            self.update_image_output()
        else:
            self.output_widget.configure(image="")

    def update_data(self):
        self.before_show()

    # **
    # ** end page stuff
    # **
    def init_image_input(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                settings.IMAGE_INPUT_FRAME_WIDTH
            )
            self.camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                settings.IMAGE_INPUT_FRAME_HEIGHT
            )
            if(self.camera.get(cv2.CAP_PROP_FPS) < 1.0):
                raise Exception("no camera found")
            while(not self.camera.isOpened()):
                pass
        except Exception as e:
            print("camera init error")
            print(e)
            self.camera = None
        except cv2.error as e:
            print("no camera found")
            print(e)
            self.camera = None

        if(self.camera is None):
            print("no camera present. disable camera button")
            self.start_camera_button.config(state=tk.DISABLED)

        return self.camera is not None

    def start_camera(self):
        if(not self.camera_running and self.camera is not None):
            self.camera_running = True
            self.update_camera_output()
        else:
            print("no camera to start")

    def pause_camera(self):
        if(self.camera is not None and self.camera_running is True):
            self.camera_running = False
            self.camera.release()

    def update_camera_output(self):
        if(self.camera_running is True and self.camera is not None):
            # capture frame
            _, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            # convert to grayscale
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.image = Image.fromarray(cv2image)
            self.update_image_output()

            self.output_widget.after(
                settings.IMAGE_INPUT_FRAME_DELAY,
                self.update_camera_output
            )

    def load_image_file(self):
        # stop camera
        self.pause_camera()

        # ask for file
        file_name = filedialog.askopenfilename(
            title="Bild laden",
            filetypes=(
                ("Images", "*.png"),
                ("all files", "*.*")
            )
        )
        if(isinstance(file_name, str) is True):
            self.image = Image.open(file_name)
            self.update_image_output()

    def update_image_output(self):
        if(self.image is not None):
            img_size = self.image.size
            new_width = settings.STANDARD_IMAGE_WIDTH
            new_height = int(settings.STANDARD_IMAGE_WIDTH * (img_size[1] / img_size[0]))
            self.image_tk = ImageTk.PhotoImage(
                image=self.image.resize((new_width, new_height))
                # image=self.image.resize((500, 282))
            )
            self.output_widget.configure(image=self.image_tk)

    def send_image(self):
        if(self.image is not None):
            self.main_ctrl.set_original_image(self.image)
            self.main_ctrl.show_page(BaselinePage)
        else:
            messagebox.showinfo("Fehler", "Bitte eine Kamera anschließen oder ein Bild öffnen")
