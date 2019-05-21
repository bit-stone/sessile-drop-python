from page.image_input_page import ImageInputPage
from page.baseline_page import BaselinePage
from page.edge_detection_page import EdgeDetectionPage
from page.fitting_page import FittingPage
from page.result_page import ResultPage


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
        page = ImageInputPage
        if(page_label == "image_input"):
            page = ImageInputPage
        elif(page_label == "baseline"):
            page = BaselinePage
        elif(page_label == "edge_detection"):
            page = EdgeDetectionPage
        elif(page_label == "fitting"):
            page = FittingPage
        elif(page_label == "result"):
            page = ResultPage
        self.main_ctrl.show_page(page)
