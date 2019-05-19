from page.image_input import ImageInputPage
from page.start import StartPage
from page.baseline import BaselinePage


class ToolbarController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None

    def connect_page(self, page):
        self.page = page

    def before_hide(self):
        pass

    def before_show(self):
        pass

    def show_page(self, page_label):
        page = StartPage
        if(page_label == "image_input"):
            page = ImageInputPage
        elif(page_label == "baseline"):
            page = BaselinePage
        self.main_ctrl.show_page(page)
