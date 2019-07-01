import numpy as np
import math
import numpy.linalg as npla

class FittingCircle:
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

        # find highest point above baseline
        points = np.concatenate((self.left_points, self.right_points))
        print(points)

        point_count = len(points)
        m = self.baseline.m
        b = self.baseline.b
        debug_count = 0
        while(point_count > 5 and debug_count <= 500):
            debug_count += 1

            def is_above(el):
                return el[0] >= m * el[1] + b

            bool_arr = np.array([is_above(row) for row in points])
            baseline_points = points[bool_arr]
            point_count = len(baseline_points)
            b += 1

        print("Anzahl Punkte: ", point_count)
        print("Durchläufe: ", debug_count)
        print("Neues b:", b)

        if(point_count == 0):
            print("Fehler: Keine Punkte für den obersten Punkt")

        # calculate average
        avg_top_point = np.average(baseline_points, axis=0)
        print(avg_top_point)

        # get left/right point on baseline
        left_point = self.left_points[np.argmin(self.left_points, axis=0)[0]]
        right_point = self.right_points[np.argmin(self.right_points, axis=0)[0]]

        self.left_contact_point = left_point
        self.right_contact_point = right_point

        avg_bottom_point = [
            (left_point[0] + right_point[0]) / 2.0,
            (left_point[1] + right_point[1]) / 2.0
        ]

        print("Links: ", left_point)
        print("Rechts: ", right_point)

        print("Basislinie: ", avg_bottom_point)

        # points until now are all in y, x
        top_bottom_vec = [
            avg_bottom_point[0] - avg_top_point[0],
            avg_bottom_point[1] - avg_top_point[1]
        ]

        top_left_vec = [
            left_point[0] - avg_top_point[0],
            left_point[1] - avg_top_point[1]
        ]

        top_right_vec = [
            right_point[0] - avg_top_point[0],
            right_point[1] - avg_top_point[1]
        ]

        top_left_angle = self.calculate_angle(top_bottom_vec, top_left_vec)
        top_right_angle = self.calculate_angle(top_bottom_vec, top_right_vec)
        print("Winkel oben-links: ", math.degrees(top_left_angle))
        print("Winkel oben-rechts: ", math.degrees(top_right_angle))

        self.left_angle = math.pi - (2 * top_left_angle)
        self.right_angle = math.pi - (2 * top_right_angle)

        angle = (self.left_angle + self.right_angle) / 2.0
        deviation = np.std([self.left_angle, self.right_angle])

        return {
            # "left": left_result,
            # "right": right_result,
            # "left_1d": left_result1d,
            # "right_1d": right_result1d,
            "left_angle": self.left_angle,
            "right_angle": self.right_angle,
            "angle": angle,
            "deviation": deviation,
            "left_contact_point": self.left_contact_point,
            "right_contact_point": self.right_contact_point,
            "flipped": False
        }

    def calculate_angle(self, vec_1, vec_2):
        result = np.dot(vec_1, vec_2) / (
            (npla.norm(vec_1)) * (npla.norm(vec_2))
        )
        result = math.acos(result)

        return result
