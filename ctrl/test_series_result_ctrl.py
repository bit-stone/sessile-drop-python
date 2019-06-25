import tkinter as tk
from tkinter import messagebox

from components.test_item import TestItem


class TestSeriesResultController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None

    def connect_page(self, page):
        self.page = page

    def before_show(self):
        pass

    def before_hide(self):
        pass
