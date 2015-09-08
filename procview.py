from processes import ProcessList
from gi.repository import Gtk
import gobject
import time


class ProcessView:
    def __init__(self):
        self.processes = ProcessList()

        self.codes = self.processes.get_proc_stats()
        types = []
        for i in self.codes:
            types.append(str)

        self.liststore = Gtk.ListStore.new(types)
        self.treeview = Gtk.TreeView(model=self.liststore)

        j = 0
        for i in self.codes:
            text = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(i, text, text=j)
            col.set_resizable(True)
            col.set_max_width(200)
            self.treeview.append_column(col)
            j += 1

        self.treeview.get_selection().connect("changed", self.on_selection)
        self.populate_proc_list()

    def on_selection(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selected_pid = model[treeiter][0]

    def populate_proc_list(self):
        t1 = time.time()
        self.processes.read()
        i = 0
        for proc in self.processes.list():
            codes = proc.status_codes
            values = [codes[c] or "" for c in self.codes]
            if i < len(self.liststore):
                self.liststore[i] = values
            else:
                self.liststore.append(values)
            i += 1
        t2 = time.time()
        print "populate proc list takes {}".format(t2 - t1)
        gobject.timeout_add(2000, self.populate_proc_list)
