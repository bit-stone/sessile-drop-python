

class EdgeDetectionController:
    def __init__(self, main_ctrl):
        self.page = None
        self.main_ctrl = main_ctrl

    # end __init__

    def connect_page(self, page):
        self.page = page
    # end connect_page

    def before_hide(self):
        pass
    # end before_hide

    def before_show(self):
        pass
    # end before_show
