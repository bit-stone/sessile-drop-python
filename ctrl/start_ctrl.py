from page.image_input import ImageInputPage


class StartController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl

    def connect_page(self, page):
        self.page = page

    def before_hide(self):
        pass

    def before_show(self):
        pass

    def show_image_input(self):
        self.main_ctrl.show_page(ImageInputPage)

    def update_label(self, label):
        label.config(text="Ich bin nur ein Test")
