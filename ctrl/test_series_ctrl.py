import tkinter as tk


class TestSeriesController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None

    def connect_page(self, page):
        self.page = page
        self.page.add_test_button.config(command=self.add_test)
        self.page.remove_test_button.config(command=self.remove_active_test)

    def before_show(self):
        pass

    def before_hide(self):
        pass

    def add_test(self):
        self.page.list.insert(tk.END, "Neuer Test")

    def remove_active_test(self):
        print(self.page.list.curselection())
        index = self.page.list.curselection()
        if(len(index) > 0):
            self.page.list.delete(index)
        pass

    def update_test_series(self):
        self.page.list.delete(0, tk.END)

        for test_item in self.main_ctrl.get_test_list():
            print(test_item)
