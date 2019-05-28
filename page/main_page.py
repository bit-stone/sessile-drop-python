import tkinter as tk

# controllers
from ctrl.main_ctrl import MainController

from ctrl.toolbar_ctrl import ToolbarController
from ctrl.test_series_ctrl import TestSeriesController

from ctrl.image_input_ctrl import ImageInputController
from ctrl.baseline_ctrl import BaselineController
from ctrl.edge_detection_ctrl import EdgeDetectionController
from ctrl.fitting_ctrl import FittingController
from ctrl.result_ctrl import ResultController

# pages
from page.toolbar_page import ToolbarPage
from page.test_series_page import TestSeriesPage

from page.image_input_page import ImageInputPage
from page.baseline_page import BaselinePage
from page.edge_detection_page import EdgeDetectionPage
from page.fitting_page import FittingPage
from page.result_page import ResultPage

# page tuple
# (page, ctrl)
page_modules = [
    (ImageInputPage, ImageInputController),
    (BaselinePage, BaselineController),
    (EdgeDetectionPage, EdgeDetectionController),
    (FittingPage, FittingController),
    (ResultPage, ResultController)
]


class SessileDropApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Main Controller must be instanciated before
        # creating the pages so they can have a reference
        # to it.
        # will be filled with pages later
        self.main_ctrl = MainController()
        self.toolbar_ctrl = ToolbarController(self.main_ctrl)
        self.test_series_ctrl = TestSeriesController(self.main_ctrl)

        self.main_ctrl.connect_test_series_ctrl(self.test_series_ctrl)

        # create first dummy test

        self.title("Sessile Drop Analysis")
        self.geometry("1350x850")

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        # Toolbar Frame
        self.button_frame = ToolbarPage(self, self.toolbar_ctrl)
        self.button_frame.grid(row=0, column=0, sticky="nw")

        # main content frame (left)
        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=1, column=0, sticky="nesw")

        # test series frame (right)
        self.test_series_frame = TestSeriesPage(self, self.test_series_ctrl)
        self.test_series_frame.grid(row=0, column=1, rowspan=2)

        self.pages = {}
        self.controllers = {}
        for (page, ctrl) in page_modules:
            ctrl_obj = ctrl(
                self.main_ctrl
            )

            page_obj = page(
                self.content_frame,
                ctrl_obj
            )

            self.pages[page] = page_obj
            self.controllers[ctrl] = ctrl_obj

            page_obj.grid(row=0, column=0)
            page_obj.grid_remove()
        # end for page, ctrl in page_modules
        self.main_ctrl.init_pages(self.pages)
        self.main_ctrl.show_page(ImageInputPage)
    # end __init__
