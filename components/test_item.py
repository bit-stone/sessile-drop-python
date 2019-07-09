import settings

from components.baseline import Baseline


class TestItem:
    def __init__(self, label="Neuer Test"):

        # General
        self.label = label

        # Image Input
        self.original_image = None  # saved
        self.original_image_tk = None

        # Baseline
        self.click_state = "needle_crop_1"
        self.scale_factor = 1.0
        self.baseline = Baseline()  # saved (first_point / second_point)

        self.drop_crop = [0, 0, 0, 0]  # saved
        self.needle_crop = [0, 0, 0, 0]  # saved

        self.baseline_coords = [0, 0, 0, 0]
        self.drop_crop_coords = [0, 0, 0, 0]
        self.needle_crop_coords = [0, 0, 0, 0]

        self.drop_image = None
        self.drop_tk_image = None

        self.needle_image = None
        self.needle_tk_image = None

        # Edge Detection
        self.edge_value_top = settings.BW_DEFAULT_THRESHOLD  # saved
        self.edge_value_bottom = 0  # saved
        self.edge_method = "bw_threshold_linear"  # saved

        self.edge_points = []
        self.edge_image = None
        self.edge_image_tk = None

        self.needle_pixel_width = 0
        self.needle_angle = 0.0

        # Fitting
        self.fluid = None  # saved
        self.fit_method = "tangent_1"  # saved
        self.left_points = []
        self.right_points = []

        self.fit_result = None

    def is_finished(self):
        return (self.fit_result is not None and self.fluid is not None)

    def get_drop_crop_height(self):
        return abs(int(self.drop_crop[3] - self.drop_crop[1]))
