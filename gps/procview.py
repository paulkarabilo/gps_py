"""
    ProcView
"""


from gi.repository import Gtk
from .processes import ProcessList
import os, signal

class ProcessView:
    def __init__(self, window):
        self.window = window
        self.processes = ProcessList()

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
        self.treeview.connect("button_release_event", self.on_process_right_click)

    def on_col_click(self, col):
        title = col.get_title()
        [what, order] = self.processes.sort_by(title)
        cols = self.treeview.get_columns()
        for c in cols:
            c.set_sort_indicator(True if c is col else False)
        col.set_sort_order(order)
        self.update()

    def on_selection(self, selection):
        model, i = selection.get_selected()
        if i is not None:
            self.selected_pid = model[i][0]

    def on_process_right_click(self, treeview, event):
        if event.button == 3:
            path, column, x, y = treeview.get_path_at_pos(int(event.x), int(event.y))
            treeview.grab_focus()
            treeview.set_cursor(path, column, 0)
            menu = Gtk.Menu()
            item = Gtk.MenuItem("Stop Process")
            item.connect("activate", self.kill_process)
            menu.append(item)
            menu.show_all()
            Gtk.Menu.popup(menu, None, None, None, None, 1, 0)

    def kill_process(self, event):
        try:
            os.kill(int(self.selected_pid), signal.SIGKILL)
            self.selected_pid = None
        except OSError:
            self.window.show_error("Error", "Could not kill process {0}".format(
                self.selected_pid))

    def destroy(self):
        self.treeview.destroy()

    def update(self):
        self.processes.read()
        i = 0
        for proc in self.processes.list():
            values = [proc[c] for c in self.codes]
            if i < len(self.liststore):
                self.liststore[i] = values
            else:
                self.liststore.append(values)
            i += 1