from gi.repository import Gtk

import os, signal

from processes import ProcessList

class GnomePSWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererText Example")
        self.set_border_width(10)
        self.set_default_size(200, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.processes = ProcessList()
        self.liststore = Gtk.ListStore(str, str)
        self.populate_proc_list()

        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.set_vexpand(True)
        self.grid.attach(self.scrollable, 0, 0, 8, 10)

        self.treeview = Gtk.TreeView(model=self.liststore)

        pid_text = Gtk.CellRendererText()
        pid_col = Gtk.TreeViewColumn("PID", pid_text, text=0)
        pid_col.set_max_width(300)
        self.treeview.append_column(pid_col)

        path_text = Gtk.CellRendererText()
        path_col = Gtk.TreeViewColumn("Path", path_text, text=1)
        path_col.set_max_width(300)
        self.treeview.append_column(path_col)

        self.treeview.get_selection().connect("changed", self.on_selection)
        self.scrollable.add(self.treeview)

        self.new_button = Gtk.Button("New Process")
        self.kill_button = Gtk.Button("Kill Process")

        self.kill_button.connect("clicked", self.on_kill_button_clicked)

        self.grid.attach_next_to(self.new_button, self.scrollable,
                Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.kill_button, self.new_button,
                Gtk.PositionType.RIGHT, 1, 1)

        self.add(self.grid)

        self.show_all()

    def populate_proc_list(self):
        self.processes.read()
        self.liststore.clear()
        for proc in self.processes.list():
            self.liststore.append([proc.pid, proc.cmdline])

    def on_selection(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selected_pid = model[treeiter][0]
            print "You selected {0}".format(model[treeiter][0])

    def on_new_button_clicked(self):
        pass

    def on_kill_button_clicked(self, button):
        if self.selected_pid:
            os.kill(int(self.selected_pid), signal.SIGKILL)
            self.populate_proc_list()
            self.selected_pid = None

win = GnomePSWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
