class Baseline:
    def __init__(self):
        self.reset_points()

    def reset_points(self):
        self.first_point = [0, 0]
        self.second_point = [0, 0]
        self.m = 0.0
        self.b = 0.0
        self.left_point = [0, 0]
        self.right_point = [0, 0]
        self.is_finished_var = False

    def set_first_point(self, point):
        self.first_point = point

    def set_second_point(self, point):
        self.second_point = point

    def calculate_params(self):
        if(self.second_point[0] < self.first_point[0]):
            self.left_point = self.second_point
            self.right_point = self.first_point
        else:
            self.left_point = self.first_point
            self.right_point = self.second_point

        dx = self.right_point[0] - self.left_point[0]
        dy = self.right_point[1] - self.left_point[1]
        dxy = (self.left_point[1] * self.right_point[0]) - self.right_point[1] * self.left_point[0]

        if(dx != 0):
            self.m = dy / dx
            self.b = dxy / dx
            self.is_finished_var = True
        else:
            self.m = 0
            self.b = 0
            self.is_finished_var = False

    def get_value(self, x):
        return self.m * x + self.b

    def is_finished(self):
        return self.is_finished_var
