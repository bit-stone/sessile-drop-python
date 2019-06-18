class TestItem:
    def __init__(self, label="Neuer Test"):
        # only core data
        self.label = label
        self.original_image = None

        self.drop_crop = [0, 0, 0, 0]
        self.drop_image = None
        self.baseline = None
        self.needle_crop = [0, 0, 0, 0]
        self.needle_image = None
        self.needle_data = None

        self.drop_edge_points = None
        self.left_points = None
        self.right_points = None

        self.edge_params = None

        self.fit_method = None
        self.fit_result = None

    def is_finished(self):
        return self.fit_result is not None
