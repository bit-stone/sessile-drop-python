import numpy as np

from components.fitting_tangent_1 import FittingTangent1
from components.fitting_circle import FittingCircle

from page.result_page import ResultPage


class FittingController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl

        self.left_angle = 0.0
        self.right_angle = 0.0

        self.left_contact_point = [0, 0]
        self.right_contact_point = [0, 0]

    def connect_page(self, page):
        self.page = page

    def before_hide(self):
        pass

    def before_show(self):
        pass

    def update_data(self):
        test = self.main_ctrl.get_current_test()
        print("Vorherige Methode:")
        print(test.fit_method)
        if(test.fit_method is not None):
            print("Setze Methode")
            self.page.method_var.set(test.fit_method)
            print(self.page.method_var.get())

    def request_fitting(self):
        # get edge points
        points = self.main_ctrl.get_edge_points()
        baseline = self.main_ctrl.get_baseline()

        # filter only points above baseline
        # el[0] -> y  - - el[1] -> x
        print(baseline)

        def is_above(el):
            return el[0] >= baseline.get_value(el[1])

        bool_arr = np.array([is_above(row) for row in points])
        baseline_points = points[bool_arr]
        # print(baseline_points)
        print("Basislinie Punkte: ", len(baseline_points))
        print(len(points))

        # seperate points for left and right side
        right_edge_point = np.amax(baseline_points, axis=0)[1]
        left_edge_point = np.amin(baseline_points, axis=0)[1]

        middle_point = int((
                (right_edge_point - left_edge_point) / 2
                ) + left_edge_point)

        left_points = baseline_points[baseline_points[:, 1] < middle_point]
        right_points = baseline_points[baseline_points[:, 1] > middle_point]

        print("Mittelpunkt: ", middle_point)
        print("Punkte links: ", len(left_points))
        print("Punkte rechts: ", len(right_points))

        self.main_ctrl.set_fitting_points(left_points, right_points)

        # eigentliches Fitting ausführen
        method = self.page.method_var.get()
        fit_result = None

        if(method == "tangent_1"):
            fitter = FittingTangent1()
            fit_result = fitter.request_fitting(left_points, right_points, baseline)
        elif(method == "circle"):
            fitter = FittingCircle()
            fit_result = fitter.request_fitting(left_points, right_points, baseline)

        if(fit_result is not None):
            self.main_ctrl.set_fit_method(method)
            self.main_ctrl.set_fit_result(fit_result)

        self.main_ctrl.show_page(ResultPage)

    def update_fitting_method(self, value):
        print(value)
