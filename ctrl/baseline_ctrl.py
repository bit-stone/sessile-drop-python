from PIL import ImageTk

IMAGE_WIDTH = 1200


class BaselineController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl
        self.canvas = None
        self.refs = None

        self.image = None
        self.image_tk = None
        self.scale_factor = 1.0

    def connect_page(self, page, canvas, canvas_refs):
        self.page = page
        self.canvas = canvas
        self.refs = canvas_refs

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_move)

    def before_hide(self):
        pass

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

        def handle_click(self, evt):
            pass

        def handle_move(self, evt):
            pass
