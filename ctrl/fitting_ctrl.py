import numpy as np
import tkinter as tk
from tkinter import messagebox

import math

from components.fitting_tangent_1 import FittingTangent1
from components.fitting_circle import FittingCircle
from components.fitting_tangent_2 import FittingTangent2

from page.result_page import ResultPage


class FittingController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl

        self.test_item = None

    def connect_page(self, page):
        self.page = page

        self.page.request_fitting_button.config(
            command=self.request_fitting
        )

        # does not work :(
        # self.page.method_selection.config(command=self.update_fitting_method)

        fluids = self.main_ctrl.get_fluids()
        fluid_options = []
        for row in fluids:
            fluid_options.append(row[0])

        self.page.fluid_selection = tk.OptionMenu(
            self.page,
            self.page.fluid_var,
            *fluid_options,
            command=self.update_fluid
        )
        self.page.fluid_selection.grid(row=8, column=0)

    def before_hide(self):
        pass

    def before_show(self):
        self.test_item = self.main_ctrl.get_current_test()

        if(self.test_item.fit_method is not None):
            self.page.method_var.set(self.test_item.fit_method)
        if(self.test_item.fluid is not None):
            self.page.fluid_var.set(self.test_item.fluid)

        self.page.needle_width_label.config(
            text="Breite: {0:.2f}px".format(self.test_item.needle_pixel_width)
        )
        self.page.needle_angle_label.config(
            text="Winkel: {0:.2f}°".format(math.degrees(self.test_item.needle_angle))
        )

    def update_data(self):
        self.before_show()

    def update_fitting_method(self, value):
        self.test_item.fit_method = value

    def update_fluid(self, value):
        self.test_item.fluid = value
        self.main_ctrl.update_test_series()

    def request_fitting(self):
        if(len(self.test_item.fit_method) == 0):
            messagebox.showinfo("Fehler", "Bitte eine Fitting-Methode auswählen")
            return

        if(self.test_item.fluid is None or len(self.test_item.fluid) == 0):
            messagebox.showinfo("Fehler", "Bitte eine Flüssigkeit auswählen")
            return

        # get edge points
        points = self.test_item.edge_points
        baseline = self.test_item.baseline

        # filter only points above baseline
        # el[0] -> y  - - el[1] -> x
        # print(baseline)

        def is_above(el):
            return el[0] >= baseline.get_value(el[1])

        bool_arr = np.array([is_above(row) for row in points])
        baseline_points = points[bool_arr]
        # print(baseline_points)
        # print("Basislinie Punkte: ", len(baseline_points))
        # print(len(points))

        # seperate points for left and right side
        right_edge_point = np.amax(baseline_points, axis=0)[1]
        left_edge_point = np.amin(baseline_points, axis=0)[1]

        middle_point = int((
                (right_edge_point - left_edge_point) / 2
                ) + left_edge_point)

        left_points = baseline_points[baseline_points[:, 1] < middle_point]
        right_points = baseline_points[baseline_points[:, 1] > middle_point]

        # print("Mittelpunkt: ", middle_point)
        # print("Punkte links: ", len(left_points))
        # print("Punkte rechts: ", len(right_points))

        # self.main_ctrl.set_fitting_points(left_points, right_points)
        self.test_item.left_points = left_points
        self.test_item.right_points = right_points

        # eigentliches Fitting ausführen
        method = self.test_item.fit_method
        fit_result = None

        if(method == "tangent_1"):
            fitter = FittingTangent1()
            fit_result = fitter.request_fitting(left_points, right_points, baseline)
        elif(method == "circle"):
            fitter = FittingCircle()
            fit_result = fitter.request_fitting(left_points, right_points, baseline)
        elif(method == "tangent_2"):
            fitter = FittingTangent2()
            fit_result = fitter.request_fitting(left_points, right_points, baseline)

        if(fit_result is not None):
            self.test_item.fit_result = fit_result

        self.main_ctrl.show_page(ResultPage)
