class MainController:
    def __init__(self):
        self.current_page = None

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
