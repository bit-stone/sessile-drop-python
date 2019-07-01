from components.test_item import TestItem
import settings
import csv

class MainController:
    def __init__(self):
        self.page_list = None
        self.current_page = None

        self.test_list = []
        self.test_index = 0

        self.test_list_ctrl = None

        # read fluids.csv
        # Format:
        # Name, IFT, Disperse, Polar, Density, Viscosity, Temperature
        self.fluids = []
        with open("fluids.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            first = True
            for row in csv_reader:
                # append row, ignoring first line as it only
                # contains title
                if(not first):
                    # convert strings to floats
                    try:
                        row[settings.FLUID_IDX_IFT] = float(row[settings.FLUID_IDX_IFT])
                        row[settings.FLUID_IDX_DISPERSE] = float(row[settings.FLUID_IDX_DISPERSE])
                        row[settings.FLUID_IDX_POLAR] = float(row[settings.FLUID_IDX_POLAR])
                        row[settings.FLUID_IDX_DENSITY] = float(row[settings.FLUID_IDX_DENSITY])
                        row[settings.FLUID_IDX_VISCOSITY] = float(row[settings.FLUID_IDX_VISCOSITY])
                        row[settings.FLUID_IDX_TEMPERATURE] = float(row[settings.FLUID_IDX_TEMPERATURE])
                    except ValueError:
                        print("Fehler beim Einlesen der Fluide.")
                        raise
                    self.fluids.append(row)
                else:
                    first = False

        # print(self.fluids)

        # create first dummy test
        self.test_list.append(TestItem("1"))



    def init_page_list(self, page_list):
        self.page_list = page_list
    # end init_page_list

    def show_page(self, page_class):
        # this page is already shown
        if(page_class is type(self.current_page)):
            return

        # show the page and run before_hide/before_show
        if(self.current_page is not None):
            self.current_page.before_hide()
        for page_index, page in self.page_list.items():
            page.grid_remove()
        page = self.page_list[page_class]
        self.current_page = page
        self.current_page.before_show()
        page.grid()
    # end show_page

    def update_page_data(self):
        if(self.page_list is not None):
            for key, page in self.page_list.items():
                page.update_data()

    def update_test_series(self):
        self.test_series_ctrl.update_test_series()

    def delete_test(self, index):
        del self.test_list[index]

    # need to connect to test series controller to update list
    def connect_test_series_ctrl(self, test_series_ctrl):
        self.test_series_ctrl = test_series_ctrl
        self.test_series_ctrl.update_test_series()
        self.test_series_ctrl.page.activate_index(0)
    # end connect_test_list_ctrl

    def set_test_index_active(self, test_index):
        self.test_index = test_index
        self.update_test_series()
    # end set_test_index_active

    def get_test_index(self):
        return self.test_index

    def add_test(self, test):
        self.test_list.append(test)
    # end add_test

    def get_test_list(self):
        return self.test_list
    # end get_test_list

    def get_current_test_label(self):
        return self.test_list[self.test_index].label
    # end get_current_test_label

    def get_current_test(self):
        return self.test_list[self.test_index]

    def get_fluids(self):
        return self.fluids

    def get_fluid_data(self, test_fluid):
        for fluid in self.fluids:
            if(fluid[0] == test_fluid):
                return fluid
        return None

    def set_original_image(self, image):
        self.test_list[self.test_index].original_image = image
    # end set_original_image

    def set_drop_image(self, image):
        self.test_list[self.test_index].drop_image = image
    # end set_drop_image

    def set_needle_image(self, image):
        self.test_list[self.test_index].needle_image = image
    # end set_drop_image

    def set_needle_data(self, needle_data):
        self.test_list[self.test_index].needle_data = needle_data
    # end set_needle_data

    def set_edge_points(self, points):
        self.test_list[self.test_index].drop_edge_points = points
    # end set_edge_points

    def set_baseline(self, baseline):
        self.test_list[self.test_index].baseline = baseline
    # end set_baseline

    def set_drop_crop(self, drop_crop):
        self.test_list[self.test_index].drop_crop = drop_crop
    # end set_drop_crop

    def set_needle_crop(self, needle_crop):
        self.test_list[self.test_index].needle_crop = needle_crop
    # end set_needle_crop

    def set_edge_params(self, edge_params):
        self.test_list[self.test_index].edge_params = edge_params
    # end set_edge_params

    def set_fitting_points(self, left_points, right_points):
        self.test_list[self.test_index].left_points = left_points
        self.test_list[self.test_index].right_points = right_points

    def set_fit_method(self, fit_method):
        self.test_list[self.test_index].fit_method = fit_method

    def set_fit_result(self, fit_result):
        self.test_list[self.test_index].fit_result = fit_result

    def set_fluid(self, fluid):
        self.test_list[self.test_index].fluid = fluid
        # update test series
        self.test_series_ctrl.update_test_series()
