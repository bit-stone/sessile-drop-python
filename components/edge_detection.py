import numpy as np
import cv2
import settings
import math
import util as util


class EdgeDetection:
    def __init__(self):
        pass

    def needle_detection(self, needle_image):
        needle_result = self.sobel_canny(
            needle_image,
            settings.SOBEL_NEEDLE_TOP,
            settings.SOBEL_NEEDLE_BOTTOM
        )

        # get middle point
        needle_left = np.amin(needle_result["points"], axis=0)[1]
        needle_right = np.amax(needle_result["points"], axis=0)[1]
        needle_middle_point = needle_right - needle_left

        # filter points to left/right
        left_needle_points = needle_result["points"][
            needle_result["points"][:, 1] <= needle_middle_point
        ]

        right_needle_points = needle_result["points"][
            needle_result["points"][:, 1] > needle_middle_point
        ]

        # reduce left/right to one average value to get distance
        needle_avg_left = np.average(left_needle_points[:, 1])
        needle_avg_right = np.average(right_needle_points[:, 1])

        needle_width = needle_avg_right - needle_avg_left

        # get angle and apply it to before mentioned distance
        # first fit line to left/right
        needle_left_fit = np.polyfit(
            left_needle_points[:, 0],
            left_needle_points[:, 1],
            1
        )

        needle_right_fit = np.polyfit(
            right_needle_points[:, 0],
            right_needle_points[:, 1],
            1
        )

        avg_m = (needle_left_fit[0] + needle_right_fit[0]) / 2.0

        needle_angle = util.calculate_angle(
            [1, 0],
            [1, avg_m]
        )

        needle_width = needle_width * math.cos(needle_angle)

        return {
            "width": needle_width,
            "angle": needle_angle
        }

    # end needle_detection
    # ##################

    def sobel_canny(
        self,
        grey_image,
        top_threshold,
        bottom_threshold
    ):
        grey_values = list(grey_image.getdata())
        grey_values = np.uint8(grey_values).reshape(
            (grey_image.size[1], grey_image.size[0])
        )

        result = cv2.Canny(
            grey_values, top_threshold, bottom_threshold
        )

        result = np.uint8(result)

        result_points = np.argwhere(result > 10)

        def flip_y(el):
            return [grey_image.size[1] - el[0], el[1]]

        result_points = np.array(list(map(flip_y, result_points)))

        return {
            "image": result,
            "points": result_points
        }
    # end sobel_canny
    # ##################

    def bw_threshold_linear(
        self,
        grey_image,
        threshold
    ):
        # turn gray into bw image
        bw_image = grey_image.point(
            lambda x: 0 if x < threshold else 255, "1"
        )
        bw_values = list(bw_image.getdata())
        bw_values = np.uint8(bw_values).reshape(
            (grey_image.size[1], grey_image.size[0])
        )

        img_size = bw_image.size
        print(img_size)

        # detect edges
        left_edges = np.zeros(img_size[1])
        right_edges = np.zeros(img_size[1])
        for row in range(img_size[1] - 1):
            left_edges[row] = np.argmax(
                bw_values[row, 0:img_size[0]] < settings.BW_LINEAR_THRESHOLD
            )

            # subpixel correction
            if(left_edges[row] != 0):
                sub_corr = (
                    settings.BW_LINEAR_THRESHOLD
                    - np.float_(bw_values[row, np.int(left_edges[row] - 1)])
                )/(
                    np.float_(bw_values[row, np.int(left_edges[row])])
                    - np.float_(bw_values[row, np.int(left_edges[row] - 1)])
                )
                left_edges[row] = left_edges[row] + sub_corr

            # right edge
            right_edges[row] = np.int(img_size[0] - np.argmax(
                bw_values[row, range(img_size[0] - 1, 0, -1)] < settings.BW_LINEAR_THRESHOLD
            ))

            # if there is no edge img_size[0] would be the result
            # make sure to ignore this by setting it 0
            if(right_edges[row] == img_size[0]):
                right_edges[row] = 0

            # subpixel correction
            if(right_edges[row] != 0):
                sub_corr = (
                    settings.BW_LINEAR_THRESHOLD
                    - np.float_(bw_values[row, np.int(right_edges[row] - 1)])
                )/(
                    np.float_(bw_values[row, np.int(right_edges[row])])
                    - np.float_(bw_values[row, np.int(right_edges[row] - 1)])
                )
                right_edges[row] = right_edges[row] + sub_corr

        # combine left and right edges to one big list of points
        edges = []
        for row in range(img_size[1] - 1):
            if(left_edges[row] != 0):
                edges.append((row, left_edges[row]))
            if(right_edges[row] != 0):
                edges.append((row, right_edges[row]))

        def flip_y(el):
            return [img_size[1] - el[0], el[1]]

        result_points = np.array(list(map(flip_y, edges)))
        # print(result_points)

        return {
            "image": bw_values,
            "points": result_points
        }
    # end bw_threshold_linear
    # ##################
