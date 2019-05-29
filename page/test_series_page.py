import tkinter as tk


class TestSeriesPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        # current test
        current_label = tk.Label(self, text="Aktueller Test:")
        current_label.grid(row=0, column=0)

        self.test_label = tk.Label(self, text="-")
        self.test_label.grid(row=1, column=0)

        # test list
        title_label = tk.Label(self, text="Bisherige Tests:")
        title_label.grid(row=10, column=0, pady=(50, 5))

        self.list = tk.Listbox(self)
        self.list.grid(row=15, column=0)

        # test list actions
        self.show_test_button = tk.Button(self, text="Markierten Test öffnen")
        self.show_test_button.grid(row=19, column=0)

        self.remove_test_button = tk.Button(self, text="Markierten Test entfernen")
        self.remove_test_button.grid(row=20, column=0)

        # new test
        self.new_test_entry = tk.Entry(self)
        self.new_test_entry.grid(row=29, column=0, pady=(50, 5))

        self.add_test_button = tk.Button(self, text="Neuen Test hinzufügen")
        self.add_test_button.grid(row=30, column=0)

        self.ctrl.connect_page(self)

    def activate_index(self, index):
        self.list.select_clear(0, "end")
        self.list.selection_set(index)
        self.list.see(index)
        self.list.activate(index)
        self.list.selection_anchor(index)

    def before_hide(self):
        self.ctrl.before_hide()

    def before_show(self):
        self.ctrl.before_show()

    def update_data(self):
        pass
