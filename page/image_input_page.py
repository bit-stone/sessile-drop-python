import tkinter as tk


class ImageInputPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        label = tk.Label(
            self,
            text="Bildeingabe"
        )
        label.grid(row=0, column=0)

        image_label = tk.Label(self)
        image_label.grid(row=1, column=0)

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0)

        open_file_button = tk.Button(
            button_frame,
            text="Aus Datei...",
            command=lambda:
                self.ctrl.load_image_file()
        )
        open_file_button.grid(row=0, column=0)

        start_camera_button = tk.Button(
            button_frame,
            text="Kamera an",
            command=lambda:
                self.ctrl.start_camera()
        )
        start_camera_button.grid(row=0, column=1)

        send_image_button = tk.Button(
            button_frame,
            text="Übernehmen",
            command=lambda:
                self.ctrl.send_image()
        )
        send_image_button.grid(row=0, column=2)

        self.ctrl.connect_page(self, image_label, start_camera_button)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        self.ctrl.update_data()
