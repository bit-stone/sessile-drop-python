import numpy as np
import math
import numpy.linalg as npla
import settings


class FittingTangent2:
    def __init__(self):
        self.left_points = None
        self.right_points = None

        self.baseline = None

        self.left_angle = 0
        self.right_angle = 0

        self.left_contact_point = [0, 0]
        self.right_contact_point = [0, 0]

    def request_fitting(self, left_points, right_points, baseline):
        # reduce number of points
        self.left_points = left_points[left_points[:, 0].argsort()]
        self.right_points = right_points[right_points[:, 0].argsort()]

        self.left_points = self.left_points[:settings.FT2_POINT_COUNT]
        self.right_points = self.right_points[:settings.FT2_POINT_COUNT]
        self.baseline = baseline

        # extract x and y values
        left_x = self.left_points[:, 1]
        left_y = self.left_points[:, 0]

        right_x = self.right_points[:, 1]
        right_y = self.right_points[:, 0]

        # fitting
        left_result = np.polyfit(left_x, left_y, deg=settings.FT1_POLYNOM_ORDER)
        left_result1d = np.poly1d(left_result)

        right_result = np.polyfit(right_x, right_y, deg=settings.FT1_POLYNOM_ORDER)
        right_result1d = np.poly1d(right_result)

        # prepare binary search for contact point
        # left most point on baseline
        left_point = self.left_points[np.argmin(self.left_points, axis=0)[0]]
        # right most point on baseline
        right_point = self.right_points[np.argmin(self.right_points, axis=0)[0]]

        # find contact points of fitted polynoms with baseline
        self.left_contact_point = self.find_intersection_point(
            left_result1d,
            self.baseline,
            left_point,
            True
        )

        self.right_contact_point = self.find_intersection_point(
            right_result1d,
            self.baseline,
            right_point,
            False
        )

        # print("Linker Kontaktpunkt: ", left_intersection)
        # print("Rechter Kontaktpunkt: ", right_intersection)

        # get derivative of fitting polynom at contact points
        left_m = self.get_derivate_value(
            left_result,
            self.left_contact_point[1]
        )

        right_m = self.get_derivate_value(
            right_result,
            self.right_contact_point[1]
        )

        base_m = self.baseline.m

        self.left_angle = self.calculate_angle(
            [left_m, 1],
            [base_m, 1]
        )
        self.right_angle = self.calculate_angle(
            [right_m, 1],
            [base_m, 1]
        )

        angle = (self.left_angle + self.right_angle) / 2.0
        deviation = np.std([self.left_angle, self.right_angle])

        # calculate angle with baseline

        return {
            "left_angle": self.left_angle,
            "right_angle": self.right_angle,
            "angle": angle,
            "deviation": deviation,
            "left_contact_point": self.left_contact_point,
            "right_contact_point": self.right_contact_point,
            "flipped": False
        }
    # end request_fitting

    def find_intersection_point(self, poly1d, baseline, start_point, is_ascending):
        left_x = start_point[1] - settings.FT2_BIN_SEARCH_OFFSET
        right_x = start_point[1] + settings.FT2_BIN_SEARCH_OFFSET
        middle_x = start_point[1]
        delta_x = abs(right_x - left_x)
        count = 0

        print("Startwerte: ", left_x, right_x, middle_x, delta_x, count)

        while(
            count < settings.FT2_BIN_SEARCH_MAX_COUNT
            and delta_x > settings.FT2_BIN_SEARCH_DELTA_X
        ):
            count += 1
            if(poly1d(middle_x) >= baseline.get_value(middle_x)):
                if(is_ascending):
                    right_x = middle_x
                else:
                    left_x = middle_x
            else:
                if(is_ascending):
                    left_x = middle_x
                else:
                    right_x = middle_x
            delta_x = abs(right_x - left_x)
            middle_x = ((right_x - left_x) / 2.0) + left_x
        print("intersection count: ", count)
        print("found x: {0} with delta_x: {1}".format(middle_x, delta_x))
        return [baseline.get_value(middle_x), middle_x]
    # end find_intersection_point

    def get_derivate_value(self, poly, x):
        return poly[0] * x * x * 3.0 + poly[1] * x * 2.0 + poly[2]
    # end get_derivate_value

    def calculate_angle(self, vec_1, vec_2):
        result = np.dot(vec_1, vec_2) / (
            (npla.norm(vec_1)) * (npla.norm(vec_2))
        )
        result = math.acos(result)

        return result
    # end calculate_angle
