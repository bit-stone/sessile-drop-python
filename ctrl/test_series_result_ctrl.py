import tkinter as tk
from tkinter import messagebox
import settings
import numpy as np

from components.test_item import TestItem
import math


class TestSeriesResultController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.page = None
        self.plot = None
        self.canvas = None

    def connect_page(self, page):
        self.page = page
        self.canvas = page.canvas
        self.plot = page.plot

    def before_show(self):
        test_list = self.main_ctrl.get_test_list()
        x_values = []
        y_values = []
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

                print("X: {0:.5f}, Y: {1:.5f}".format(x, y))
                x_values.append(x)
                y_values.append(y)
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

        result_polar = m * m
        result_disperse = b * b

        result_total = result_polar + result_disperse

        # start drawing
        self.plot.cla()
        self.plot.scatter(
            x_values,
            y_values,
            marker="+",
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
                result_polar, result_disperse, result_total
            )
        )

    # end before_show

    def before_hide(self):
        pass
