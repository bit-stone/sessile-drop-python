from page.result_page import ResultPage


class FittingController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl

        self.left_angle = 0.0
        self.right_angle = 0.0

        self.left_contact_point = [0, 0]
        self.right_contact_point = [0, 0]

    def connect_page(self, page):
        self.page = page

    def before_hide(self):
        pass

    def before_show(self):
        pass

    def request_fitting(self):
        self.main_ctrl.show_page(ResultPage)

    def update_fitting_method(self, value):
        print(value)
