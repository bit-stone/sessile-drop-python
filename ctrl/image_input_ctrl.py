import cv2
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import util as util

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
        self.camera_image = None
        self.camera_image_tk = None

        self.test_item = None

    def connect_page(self, page):
        self.page = page
        self.output_widget = page.image_label

        self.page.open_file_button.config(command=self.load_image_file)
        self.page.start_camera_button.config(command=self.start_camera)
        self.page.capture_camera_button.config(command=self.capture_camera_output)
        self.page.send_image_button.config(command=self.send_image)

        self.init_image_input()

    def before_hide(self):
        self.pause_camera()

    def before_show(self):
        if(self.camera is not None and self.camera.isOpened() is not True):
            self.init_image_input()

        self.test_item = self.main_ctrl.get_current_test()

        if(self.test_item.original_image is not None):
            self.update_image_output()
        else:
            self.output_widget.configure(image="")

    def update_data(self):
        self.before_show()

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
            self.page.start_camera_button.config(state=tk.DISABLED)
            self.page.capture_camera_button.config(state=tk.DISABLED)

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
            self.camera_image = Image.fromarray(cv2image)
            self.camera_image = ImageOps.flip(self.camera_image)
            self.update_image_output()

            self.output_widget.after(
                settings.IMAGE_INPUT_FRAME_DELAY,
                self.update_camera_output
            )

    def capture_camera_output(self):
        self.test_item.original_image = self.camera_image
        self.pause_camera()
        self.update_image_output()

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
            self.test_item.original_image = Image.open(file_name)
            self.update_image_output()

    def update_image_output(self):
        if(self.camera_running is True):
            self.camera_image_tk = util.image_to_widget(
                self.camera_image, self.output_widget
            )
        else:
            self.test_item.original_image_tk = util.image_to_widget(
                self.test_item.original_image, self.output_widget
            )
            print(self.test_item.original_image_tk)

    def send_image(self):
        if(self.test_item.original_image is not None):
            self.pause_camera()
            self.main_ctrl.show_page(BaselinePage)
        else:
            messagebox.showinfo("Fehler", "Der Test benötigt ein gültiges Bild.")
