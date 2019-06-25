import tkinter as tk
from tkinter import messagebox

from components.test_item import TestItem

from page.image_input_page import ImageInputPage
from page.test_series_result_page import TestSeriesResultPage


class TestSeriesController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None

    def connect_page(self, page):
        self.page = page
        self.page.add_test_button.config(command=self.add_test)
        self.page.remove_test_button.config(command=self.remove_active_test)
        self.page.show_test_button.config(command=self.open_active_test)
        self.page.series_result_button.config(command=self.show_series_result)

    def before_show(self):
        pass

    def before_hide(self):
        pass

    def add_test(self):
        new_label = self.page.new_test_entry.get()
        if(len(new_label) > 0):
            self.page.list.insert(tk.END, new_label)
            self.page.new_test_entry.delete(0, tk.END)
            new_index = (len(self.page.list.get(0, tk.END)) - 1)
            print(new_index)
            new_test = TestItem(new_label)
            self.main_ctrl.add_test(new_test)
            self.main_ctrl.set_test_index_active(new_index)
            self.main_ctrl.update_page_data()
            self.page.activate_index(new_index)
            self.main_ctrl.show_page(ImageInputPage)
        else:
            messagebox.showinfo("Bitte einen Namen vergeben", "Bitte dem neuen Test einen Namen geben")

    def remove_active_test(self):
        confirm_delete = messagebox.askokcancel(
            "Test entfernen",
            "Möchten Sie diesen Test wirklich entfernen? Er kann danach nicht wiederhergestellt werden."
        )
        if(confirm_delete):
            index = self.page.list.curselection()
            if(len(index) > 0):
                self.page.list.delete(index)
                self.main_ctrl.delete_test(index[0])
        pass

    def open_active_test(self):
        index = self.page.list.curselection()
        if(len(index) > 0):
            index = index[0]
            if(self.main_ctrl.get_test_index() != index):
                print("opening test ", index)
                self.main_ctrl.set_test_index_active(index)
                self.main_ctrl.update_page_data()
                self.page.activate_index(index)
            self.main_ctrl.show_page(ImageInputPage)

    def update_test_series(self):
        self.page.list.delete(0, tk.END)

        for test_item in self.main_ctrl.get_test_list():
            label = test_item.label
            if(test_item.fluid is not None):
                label = label + " (" + test_item.fluid + ")"
            self.page.list.insert(tk.END, label)

        self.page.test_label.config(text=self.main_ctrl.get_current_test_label())

    def show_series_result(self):
        try:
            # check whether needle diameter is set
            try:
                needle_diameter = float(self.page.needle_entry.get())
            except ValueError:
                raise ValueError("Bitte einen gültigen Nadeldurchmesser in mm angeben (Format 1.234)")

            # need at least one test
            test_list = self.main_ctrl.get_test_list()
            if(len(test_list) < 1):
                raise ValueError("Bitte mindestens einen Test hinzufügen")

            # check all tests for readiness (must all be finished)
            for test in test_list:
                if(test.is_finished() is not True):
                    raise ValueError("Alle Tests müssen abgeschlossen sein. " + test.label + " ist noch nicht abgeschlossen")


            self.main_ctrl.show_page(TestSeriesResultPage)

        except ValueError as err:
            messagebox.showinfo("Fehler", err)
