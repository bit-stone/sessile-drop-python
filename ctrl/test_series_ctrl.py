import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import os
from os.path import isfile, join

import settings
import csv
from PIL import Image

import util as util

from components.test_item import TestItem
from components.baseline import Baseline

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
        self.page.load_button.config(command=self.load_series)

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
        if(len(self.page.list.get(0, tk.END)) > 1):
            confirm_delete = messagebox.askokcancel(
                "Test entfernen",
                "Möchten Sie diesen Test wirklich entfernen? Er kann danach nicht wiederhergestellt werden."
            )
            if(confirm_delete):
                index = self.page.list.curselection()
                if(len(index) > 0):
                    self.page.list.delete(index)
                    self.main_ctrl.delete_test(index[0])

                    # open first test
                    self.main_ctrl.set_test_index_active(0)
                    self.main_ctrl.update_page_data()
                    self.page.activate_index(0)

        else:
            messagebox.showinfo("Fehler", "Es muss mindestens einen Test geben")

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
            if(test_item.fluid is not None and test_item.fluid != ""):
                label = label + " (" + test_item.fluid + ")"
            self.page.list.insert(tk.END, label)

        self.page.test_label.config(
            text=self.main_ctrl.get_current_test_label())

    def show_series_result(self):
        try:
            # check whether needle diameter is set or not
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

    def load_series(self):
        try:
            dirname = filedialog.askdirectory()
            print(dirname)

            filelist = os.listdir(dirname)
            print(filelist)

            # read test file
            test_file_path = join(dirname, settings.TEST_RESULT_FILE_NAME)
            print(test_file_path)
            if isfile(test_file_path):
                print("found test file")
            else:
                raise Exception("Keine Test-Datei gefunden ("+settings.TEST_RESULT_FILE_NAME+")")

            test_list = []
            with open(test_file_path, "r") as test_csv_file:
                reader = csv.reader(test_csv_file, delimiter=";")
                is_first = True
                for row in reader:
                    if(is_first):
                        is_first = False
                        if(len(row) != settings.TEST_SERIES_FILE_COL_COUNT):
                            raise Exception("Test-Datei hat eine ungültige Anzahl Spalten")
                    else:
                        test_list.append(row)

            if(len(test_list) < 1):
                raise Exception("Keine Tests gefunden")

            # check if all images exist
            for row in test_list:
                if(not isfile(join(dirname, row[0] + ".png"))):
                    raise Exception("Nicht jeder Test hat ein Bild")

            # load images and create test items
            test_item_list = []
            for row in test_list:
                test = TestItem()

                # load image
                test.original_image = Image.open(
                    join(dirname, row[settings.SAVE_IDX_INDEX] + ".png"))

                # set core data
                test.label = row[settings.SAVE_IDX_LABEL]
                test.fluid = row[settings.SAVE_IDX_FLUID]
                test.fit_method = row[settings.SAVE_IDX_FIT_METHOD]

                test.edge_method = row[settings.SAVE_IDX_EDGE_METHOD]

                edge_values = self.convert_str_to_int(
                    row[settings.SAVE_IDX_EDGE_TOP_BOTTOM]
                )
                test.edge_value_top = int(edge_values[0])
                test.edge_value_bottom = int(edge_values[1])

                test.drop_crop = self.convert_str_to_int(
                    row[settings.SAVE_IDX_DROP_CROP]
                )
                test.needle_crop = self.convert_str_to_int(
                    row[settings.SAVE_IDX_NEEDLE_CROP]
                )

                baseline = Baseline()
                baseline_points = self.convert_str_to_int(
                    row[settings.SAVE_IDX_BASELINE_FIRST_SECOND]
                )

                baseline.set_first_point(
                    [baseline_points[0], baseline_points[1]]
                )
                baseline.set_second_point(
                    [baseline_points[2], baseline_points[3]]
                )
                baseline.calculate_params()

                test.baseline = baseline

                # create cropped images
                test.drop_image = util.generate_cropped_image(
                    image=test.original_image,
                    crop=test.drop_crop
                )

                test.needle_image = util.generate_cropped_image(
                    image=test.original_image,
                    crop=test.needle_crop
                )

                # edge detection
                needle_data = self.main_ctrl.edge_detection.needle_detection(
                    test.needle_image
                )
                test.needle_pixel_width = needle_data["width"]
                test.needle_angle = needle_data["angle"]

                drop_data = self.main_ctrl.edge_detection.request_edge_detection(
                    test.drop_image,
                    test.edge_method,
                    test.edge_value_top,
                    test.edge_value_bottom
                )
                test.edge_points = drop_data["points"]

                # do fitting
                points = util.process_fitting_points(
                    test.edge_points,
                    test.baseline
                )

                test.left_points = points["left_points"]
                test.right_points = points["right_points"]

                print(test.fit_method)
                fitter = self.main_ctrl.fitter[test.fit_method]
                print(fitter)
                fit_result = fitter.request_fitting(
                    test.left_points,
                    test.right_points,
                    test.baseline
                )

                test.fit_result = fit_result

                test_item_list.append(test)

            # print(test_item_list)
            self.main_ctrl.set_test_list(test_item_list)
            self.main_ctrl.set_test_index_active(0)
            self.main_ctrl.update_page_data()

        except Exception as e:
            print(e)
            messagebox.showinfo("Fehler", e)

    def convert_str_to_int(self, str):
        result = list(map(int, str.strip("[]").split(",")))
        print(result)
        return result
