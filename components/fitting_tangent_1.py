import numpy as np
import math
import numpy.linalg as npla
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
        # first get max y value for left/right and average it
        left_max = self.left_points[np.argmax(self.left_points, axis=0)[0]][0]
        right_max = self.right_points[np.argmax(self.right_points, axis=0)[0]][0]
        avg_max = int((left_max + right_max) / 2.0)

        # left most point on baseline
        left_point = self.left_points[np.argmin(self.left_points, axis=0)[0]]
        # right most point on baseline
        right_point = self.right_points[np.argmin(self.right_points, axis=0)[0]]

        avg_middle_point = left_point[0] + (right_point[0] - left_point[0])

        dist_left_right = right_point[1] - left_point[1]
        dist_top_bottom = avg_max - avg_middle_point

        flipped = (dist_top_bottom / dist_left_right) > settings.FT1_FLIP_THRESHOLD

        # shift left pixels to left point
        def shift_left(el):
            return [el[0] - left_point[0], el[1] - left_point[1]]

        left_points = np.array(list(map(shift_left, self.left_points)))

        def shift_right(el):
            return [-(right_point[0] - el[0]), right_point[1] - el[1]]

        right_points = np.array(list(map(shift_right, self.right_points)))

        print("Nach Shifting:")
        self.left_points = left_points[left_points[:, 0].argsort()]
        self.right_points = right_points[right_points[:, 0].argsort()]

        self.left_points = self.left_points[:settings.FT1_POINT_COUNT]
        self.right_points = self.right_points[:settings.FT1_POINT_COUNT]

        # self.left_points = left_points[-settings.FT1_POINT_COUNT:]
        # self.right_points = right_points[-settings.FT1_POINT_COUNT:]

        # print("Links: ", left_point)
        # print("Rechts: ", right_point)
        # print("Höhe / Breite: ", (dist_top_bottom / dist_left_right))
        print("Sollte geflippt werden: ", flipped, settings.FT1_FLIP_THRESHOLD)

        # fit left side - first coord is the row -> y
        left_x = self.left_points[:, 1]
        left_y = self.left_points[:, 0]

        # polyfit
        if(flipped):
            left_result = np.polyfit(left_y, left_x, deg=settings.FT1_POLYNOM_ORDER)
            left_result1d = np.poly1d(left_result)
        else:
            left_result = np.polyfit(left_x, left_y, deg=settings.FT1_POLYNOM_ORDER)
            left_result1d = np.poly1d(left_result)

        # fit right side
        right_x = self.right_points[:, 1]
        right_y = self.right_points[:, 0]
        #
        # # polyfit
        if(flipped):
            right_result = np.polyfit(right_y, right_x, deg=settings.FT1_POLYNOM_ORDER)
            right_result1d = np.poly1d(right_result)
        else:
            right_result = np.polyfit(right_x, right_y, deg=settings.FT1_POLYNOM_ORDER)
            right_result1d = np.poly1d(right_result)

        # get m
        print(left_result, right_result)
        left_m = left_result[settings.FT1_POLYNOM_ORDER - 1]
        right_m = right_result[settings.FT1_POLYNOM_ORDER - 1]
        base_m = baseline.m

        print("Steigungen")
        print(left_m, right_m, base_m)

        base_vec = (1, base_m)
        if(flipped):
            left_vec = (left_m, 1)
            right_vec = (right_m, 1)
        else:
            left_vec = (1, left_m)
            right_vec = (1, right_m)

        # calculate angles
        left_angle = self.calculate_angle(left_vec, base_vec)
        right_angle = self.calculate_angle(right_vec, base_vec)

        print("Links: ", math.degrees(left_angle))
        print("Rechts: ", math.degrees(right_angle))

        angle = (left_angle + right_angle) / 2.0
        deviation = np.std([left_angle, right_angle])

        return {
            # "left": left_result,
            # "right": right_result,
            # "left_1d": left_result1d,
            # "right_1d": right_result1d,
            "left_angle": left_angle,
            "right_angle": right_angle,
            "angle": angle,
            "deviation": deviation,
            "left_contact_point": left_point,
            "right_contact_point": right_point,
            "flipped": flipped
        }

    def calculate_angle(self, vec_1, vec_2):
        result = np.dot(vec_1, vec_2) / (
            (npla.norm(vec_1)) * (npla.norm(vec_2))
        )
        result = math.acos(result)

        return result
