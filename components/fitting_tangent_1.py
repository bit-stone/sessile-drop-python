import numpy as np
import settings

class FittingTangent1:
    def __init__(self):
        self.left_points = None
        self.right_points = None

        self.baseline = None

        self.left_angle = None
        self.right_angle = None

        self.left_contact_point = [0, 0]
        self.right_contact_point = [0, 0]

    def request_fitting(self, left_points, right_points, baseline):
        self.left_points = left_points
        self.right_points = right_points
        self.baseline = baseline

        # determine whether points need to flip x/y for fitting
        # TODO

        # fit left side
        left_x = left_points[: ,0]
        left_y = left_points[: ,1]

        # polyfit
        left_result = np.polyfit(left_y, left_x, deg=settings.FT1_POLYNOM_ORDER)
        left_result1d = np.poly1d(left_result)

        # fit right side
        right_x = right_points[: ,0]
        right_y = right_points[: ,1]

        # polyfit 
        right_result = np.polyfit(right_y, right_x, deg=settings.FT1_POLYNOM_ORDER)
        right_result1d = np.poly1d(right_result)

        return {
            "left": left_result,
            "right": right_result,
            "left_1d": left_result1d,
            "right_1d": right_result1d
        }
