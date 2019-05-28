class TestItem:
    def __init__(self):
        self.label = "Neuer Test"
        self.original_image = None
        self.original_tk_image = None

        self.drop_image = None
        self.baseline = None

        self.drop_edge_points = None
        self.left_points = None
        self.right_points = None

        self.fit_result = None

    def init_with_values(self, values):
        self.original_image = values["original_image"]
        self.original_tk_image = values["original_tk_image"]

        self.drop_image = values["drop_image"]
        self.baseline = values["baseline"]

        self.drop_edge_points = values["drop_edge_points"]
        self.left_points = values["left_points"]
        self.right_points = values["right_points"]

        self.fit_result = values["fit_result"]
