import tkinter as tk


class ImageInputPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        label = tk.Label(
            self,
            text="Bildeingabe",
            font=("", 15)
        )
        label.grid(row=0, column=0)

        self.image_label = tk.Label(self)
        self.image_label.grid(row=1, column=0)

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0)

        self.open_file_button = tk.Button(
            button_frame,
            text="Aus Datei..."
        )
        self.open_file_button.grid(row=0, column=0)

        self.start_camera_button = tk.Button(
            button_frame,
            text="Kamera an"
        )
        self.start_camera_button.grid(row=0, column=1, padx=(100,5))

        self.capture_camera_button = tk.Button(
            button_frame,
            text="Aufname"
        )
        self.capture_camera_button.grid(row=0, column=2)

        self.send_image_button = tk.Button(
            button_frame,
            text="Weiter"
        )
        self.send_image_button.grid(row=0, column=3, padx=(100, 5))

        self.ctrl.connect_page(self)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        self.ctrl.update_data()
