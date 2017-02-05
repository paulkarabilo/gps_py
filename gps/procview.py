"""
    ProcView
"""


from gi.repository import Gtk, GObject
from .processes import ProcessList


class ProcessView:
    def __init__(self, window):
        self.window = window
        self.processes = ProcessList()
        self.timeout_id = None
        self.codes = self.processes.get_proc_stats()
        types = self.processes.get_proc_types()

        self.liststore = Gtk.ListStore.new(types)
        self.treeview = Gtk.TreeView(model=self.liststore)

        j = 0
        for i in self.codes:
            text = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(i, text, text=j)
            col.connect("clicked", self.on_col_click)
            col.set_resizable(True)
            col.set_clickable(True)
            col.set_max_width(200)
            self.treeview.append_column(col)
            j += 1

        self.treeview.get_selection().connect("changed", self.on_selection)
        self.populate_proc_list()

    def on_col_click(self, col):
        title = col.get_title()
        [what, order] = self.processes.sort_by(title)
        cols = self.treeview.get_columns()
        for c in cols:
            c.set_sort_indicator(True if c is col else False)
        col.set_sort_order(order)
        self.populate_proc_list()

    def on_selection(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selected_pid = model[treeiter][0]

    def populate_proc_list(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.processes.read()
        i = 0
        for proc in self.processes.list():
            values = [proc.get_attr(c) for c in self.codes]
            if i < len(self.liststore):
                self.liststore[i] = values
            else:
                self.liststore.append(values)
            i += 1
        self.timeout_id = GObject.timeout_add(2000, self.populate_proc_list)
