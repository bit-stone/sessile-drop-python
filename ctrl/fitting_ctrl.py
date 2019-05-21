class FittingController:
    def __init__(self, main_ctrl):
        self.page = None,
        self.main_ctrl = main_ctrl

    def connect_page(self, page):
        self.page = page

    def before_hide(self):
        pass

    def before_show(self):
        pass
