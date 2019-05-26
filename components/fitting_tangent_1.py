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
        # first get max y value for left/right and average it
        left_max = self.left_points[np.argmax(self.left_points, axis=0)[0]][0]
        right_max = self.right_points[np.argmax(self.right_points, axis=0)[0]][0]
        avg_max = int((left_max + right_max) / 2.0)

        # ### TODO ###
        # use actual contact points with baseline!!
        # ############
        # left most point
        left_point = self.left_points[np.argmin(self.left_points, axis=0)[0]]
        # right most point
        right_point = self.right_points[np.argmin(self.right_points, axis=0)[0]]
        # ### TODO ###
        # use actual contact points with baseline!!
        # ############

        avg_middle_point = left_point[0] + (right_point[0] - left_point[0])

        dist_left_right = right_point[1] - left_point[1]
        dist_top_bottom = avg_max - avg_middle_point

        flipped = (dist_top_bottom / dist_left_right) > settings.FT1_FLIP_THRESHOLD

        # print("Links: ", left_point)
        # print("Rechts: ", right_point)
        # print("Höhe / Breite: ", (dist_top_bottom / dist_left_right))
        print("Sollte geflippt werden: ", flipped, settings.FT1_FLIP_THRESHOLD)

        # fit left side - first coord is the row -> y
        left_x = left_points[:, 1]
        left_y = left_points[:, 0]

        # polyfit
        if(flipped):
            left_result = np.polyfit(left_y, left_x, deg=settings.FT1_POLYNOM_ORDER)
            left_result1d = np.poly1d(left_result)
        else:
            left_result = np.polyfit(left_x, left_y, deg=settings.FT1_POLYNOM_ORDER)
            left_result1d = np.poly1d(left_result)

        # fit right side
        right_x = right_points[:, 1]
        right_y = right_points[:, 0]
        #
        # # polyfit
        if(flipped):
            right_result = np.polyfit(right_y, right_x, deg=settings.FT1_POLYNOM_ORDER)
            right_result1d = np.poly1d(right_result)
        else:
            right_result = np.polyfit(right_x, right_y, deg=settings.FT1_POLYNOM_ORDER)
            right_result1d = np.poly1d(right_result)

        return {
            "left": left_result,
            "right": right_result,
            "left_1d": left_result1d,
            "right_1d": right_result1d,
            "flipped": flipped
        }
