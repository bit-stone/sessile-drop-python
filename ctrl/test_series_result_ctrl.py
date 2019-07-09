import tkinter as tk
from tkinter import messagebox
import settings
import numpy as np

from components.test_item import TestItem
import math

import os
import time
import csv


class TestSeriesResultController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None
        self.plot = None
        self.canvas = None
        self.result_polar = None
        self.result_disperse = None
        self.result_total = None

    def connect_page(self, page):
        self.page = page
        self.canvas = page.canvas
        self.plot = page.plot

        self.page.save_button.config(command=self.save_series)

    def before_show(self):
        test_list = self.main_ctrl.get_test_list()
        x_values = []
        y_values = []
        dy_values = []
        for test in test_list:
            fluid_data = self.main_ctrl.get_fluid_data(test.fluid)
            if(fluid_data is not None):
                # calculate x,y based on fluid and angle
                x = (
                    math.sqrt(fluid_data[settings.FLUID_IDX_POLAR])
                    / math.sqrt(fluid_data[settings.FLUID_IDX_DISPERSE])
                )

                y = (
                    (1.0 + math.cos(test.fit_result["angle"]))
                    * (
                        (fluid_data[settings.FLUID_IDX_IFT])
                        / (
                            2.0 * math.sqrt(fluid_data[settings.FLUID_IDX_DISPERSE])
                        )
                    )
                )

                # calculate deviation values
                # dx has no deviation
                dy1 = (
                    (1.0 + math.cos(test.fit_result["angle"] + test.fit_result["deviation"]))
                    * (
                        (fluid_data[settings.FLUID_IDX_IFT])
                        / (
                            2.0 * math.sqrt(fluid_data[settings.FLUID_IDX_DISPERSE])
                        )
                    )
                )

                dy2 = (
                    (1.0 + math.cos(test.fit_result["angle"] - test.fit_result["deviation"]))
                    * (
                        (fluid_data[settings.FLUID_IDX_IFT])
                        / (
                            2.0 * math.sqrt(fluid_data[settings.FLUID_IDX_DISPERSE])
                        )
                    )
                )

                dy = abs(dy2 - dy1) / 2.0

                print("DY1: {0:.8f} - DY2: {1:.8f}".format(dy1, dy2))
                print("X: {0:.8f}, Y: {1:.8f}".format(x, y))
                x_values.append(x)
                y_values.append(y)
                dy_values.append(dy)
            else:
                print("Fehler: Ungültiges Fluid " + test.fluid)
        # end for test in test_list
        print(x_values, y_values)
        x_values = np.array(x_values)
        y_values = np.array(y_values)

        z = np.polyfit(x_values, y_values, 1)
        z_1d = np.poly1d(z)

        m = z[0]
        b = z[1]

        self.result_polar = m * m
        self.result_disperse = b * b

        self.result_total = self.result_polar + self.result_disperse

        # start drawing
        self.plot.cla()
        # self.plot.scatter(
        #     x_values,
        #     y_values,
        #     marker="+",
        #     color="r"
        # )
        self.plot.errorbar(
            x_values,
            y_values,
            dy_values,
            marker=".",
            linestyle="None",
            capsize=3,
            color="r"
        )

        line_x = np.arange(0, 2, 0.01)
        self.plot.plot(
            line_x,
            z_1d(line_x)
        )

        self.plot.grid(
            True
        )

        self.plot.set_title("Gesamtergebnis")
        self.canvas.draw()

        self.page.line_label.config(
            text="Steigung: {0:.5f}, Achsenabschnitt: {1:.5f}".format(
                m, b
            )
        )

        self.page.result_label.config(
            text="Polar: {0:.5f}, Dispers: {1:.5f}, Total: {2:.5f}".format(
                self.result_polar, self.result_disperse, self.result_total
            )
        )

    # end before_show

    def save_series(self):
        time_label = time.strftime("%Y%m%d_%H%M%S")
        dir_path = "test_series_data/test_series_" + time_label

        test_list = self.main_ctrl.get_test_list()

        params_list = []

        print("Testserie speichern")
        print("Zeitpunkt: " + time_label)
        try:
            # check if all tests are finished
            for test in test_list:
                if(not test.is_finished()):
                    print("Alle Tests müssen abgeschlossen sein!")
                    raise ValueError()

            # create directory
            os.mkdir(dir_path)

            # title lines for csv
            label_list = [None] * settings.TEST_SERIES_FILE_COL_COUNT

            label_list[settings.SAVE_IDX_INDEX] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_INDEX]
            label_list[settings.SAVE_IDX_LABEL] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_LABEL]
            label_list[settings.SAVE_IDX_FLUID] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_FLUID]
            label_list[settings.SAVE_IDX_FIT_METHOD] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_FIT_METHOD]
            label_list[settings.SAVE_IDX_EDGE_METHOD] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_EDGE_METHOD]
            label_list[settings.SAVE_IDX_EDGE_TOP_BOTTOM] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_EDGE_TOP_BOTTOM]
            label_list[settings.SAVE_IDX_DROP_CROP] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_DROP_CROP]
            label_list[settings.SAVE_IDX_NEEDLE_CROP] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_NEEDLE_CROP]
            label_list[settings.SAVE_IDX_BASELINE_FIRST_SECOND] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_BASELINE_FIRST_SECOND]
            label_list[settings.SAVE_IDX_ANGLE] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_ANGLE]
            label_list[settings.SAVE_IDX_DEVIATION] = settings.SAVE_COL_LABELS[settings.SAVE_IDX_DEVIATION]

            params_list.append(label_list)

            # save images and gather test data
            for index, test in enumerate(test_list):
                test.original_image.save(dir_path + "/" + str(index) + ".png")

                test_list = [None] * settings.TEST_SERIES_FILE_COL_COUNT

                test_list[settings.SAVE_IDX_INDEX] = index
                test_list[settings.SAVE_IDX_LABEL] = test.label
                test_list[settings.SAVE_IDX_FLUID] = test.fluid
                test_list[settings.SAVE_IDX_FIT_METHOD] = test.fit_method
                test_list[settings.SAVE_IDX_EDGE_METHOD] = test.edge_method
                test_list[settings.SAVE_IDX_EDGE_TOP_BOTTOM] = str([test.edge_value_top, test.edge_value_bottom])
                test_list[settings.SAVE_IDX_DROP_CROP] = str(test.drop_crop)
                test_list[settings.SAVE_IDX_NEEDLE_CROP] = str(test.needle_crop)
                test_list[settings.SAVE_IDX_BASELINE_FIRST_SECOND] = str(test.baseline.first_point + test.baseline.second_point)
                test_list[settings.SAVE_IDX_ANGLE] = test.fit_result["angle"]
                test_list[settings.SAVE_IDX_DEVIATION] = test.fit_result["deviation"]

                params_list.append(test_list)

            with open(dir_path + "/" + settings.TEST_RESULT_FILE_NAME, "w") as csv_file:
                # write params
                writer = csv.writer(
                    csv_file, delimiter=";"
                )
                for line in params_list:
                    writer.writerow(line)

            # save result of complete series result
            with open(dir_path + "/" + settings.TEST_SERIES_RESULT_FILE_NAME, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                writer.writerow([
                    "result_polar", "result_disperse", "result_total"
                ])
                writer.writerow([
                    self.result_polar, self.result_disperse, self.result_total
                ])


        except ValueError:
            print("Etwas ist schief gelaufen")

    def before_hide(self):
        pass
