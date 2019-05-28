import tkinter as tk


class TestSeriesPage(tk.Frame):
    def __init__(self, parent, ctrl):
        tk.Frame.__init__(self, parent)
        self.ctrl = ctrl

        title_label = tk.Label(self, text="Testreihe:")
        title_label.grid(row=0, column=0)

        self.remove_test_button = tk.Button(self, text="Entfernen")
        self.remove_test_button.grid(row=1, column=0)

        self.list = tk.Listbox(self)
        self.list.insert(tk.END, "Test #1")
        self.list.insert(tk.END, "Test #2")
        self.list.insert(tk.END, "Test #3")
        self.list.insert(tk.END, "Test #4")
        self.list.grid(row=2, column=0)

        self.activate_index(0)

        self.add_test_button = tk.Button(self, text="+ Test")
        self.add_test_button.grid(row=3, column=0)

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
