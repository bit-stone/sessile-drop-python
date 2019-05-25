import numpy as np

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
        print(baseline_points)
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

        self.main_ctrl.show_page(ResultPage)

    def update_fitting_method(self, value):
        print(value)
