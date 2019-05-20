import cv2
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk

from page.start import StartPage
from page.baseline import BaselinePage

IMAGE_INPUT_FRAME_WIDTH = 1280
IMAGE_INPUT_FRAME_HEIGHT = 720

IMAGE_CANVAS_WIDTH = 500

IMAGE_INPUT_FRAME_DELAY = 20


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

    # **
    # ** end page stuff
    # **

    def show_start_page(self):
        self.main_ctrl.show_page(StartPage)

    def init_image_input(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                IMAGE_INPUT_FRAME_WIDTH
            )
            self.camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                IMAGE_INPUT_FRAME_HEIGHT
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
            print("test")
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
            self.image_tk = ImageTk.PhotoImage(
                image=self.image.resize((500, 282))
            )
            self.output_widget.configure(image=self.image_tk)
            self.output_widget.after(
                IMAGE_INPUT_FRAME_DELAY,
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
        self.image = Image.open(file_name)
        self.image_tk = ImageTk.PhotoImage(image=self.image.resize((500, 282)))
        self.output_widget.configure(image=self.image_tk)

    def send_image(self):
        if(self.image is not None):
            self.main_ctrl.set_original_image(self.image)
            self.main_ctrl.show_page(BaselinePage)
        else:
            print("no image to send")
