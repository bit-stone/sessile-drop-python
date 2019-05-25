class MainController:
    def __init__(self):
        self.current_page = None

        self.original_image = None
        self.original_tk_image = None

        self.drop_image = None
        self.needle_image = None

        self.baseline = None

        self.drop_edge_points = None
        self.left_points = None
        self.right_points = None

    def init_pages(self, pages):
        self.pages = pages
    # end init_pages

    def show_page(self, page_class):
        # this page is already shown
        if(page_class is type(self.current_page)):
            return

        # show the page and run before_hide/before_show
        if(self.current_page is not None):
            self.current_page.before_hide()
        for page_index, page in self.pages.items():
            page.grid_remove()
        page = self.pages[page_class]
        self.current_page = page
        self.current_page.before_show()
        page.grid()
    # end show_page

    def set_original_image(self, image):
        self.original_image = image
    # end set_original_image

    def get_original_image(self):
        return self.original_image
    # end get_original_image

    def set_drop_image(self, image):
        self.drop_image = image
    # end set_drop_image

    def get_drop_image(self):
        return self.drop_image
    # end get_drop_image

    def set_edge_points(self, points):
        self.drop_edge_points = points
    # end set_edge_points

    def get_edge_points(self):
        return self.drop_edge_points
    # end get_edge_points

    def set_baseline(self, baseline):
        self.baseline = baseline
    # end set_baseline

    def get_baseline(self):
        return self.baseline
    # end get_baseline

    def set_fitting_points(self, left_points, right_points):
        self.left_points = left_points
        self.right_points = right_points

    def get_fitting_points(self):
        return {
            "left": self.left_points,
            "right": self.right_points
        }
