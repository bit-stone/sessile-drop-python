import tkinter as tk
from tkinter import messagebox
import settings

from components.test_item import TestItem


class TestSeriesResultController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None

    def connect_page(self, page):
        self.page = page

    def before_show(self):
        test_list = self.main_ctrl.get_test_list()
        for test in test_list:
            fluid_data = self.main_ctrl.get_fluid_data(test.fluid)
            if(fluid_data is not None):
                print(test.fit_result)
            else:
                print("Fehler: Ungültiges Fluid " + test.fluid)

    def before_hide(self):
        pass
