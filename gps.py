from gi.repository import Gtk, Gdk, GLib

import gobject
import os
import signal
import time
import threading

from processes import ProcessList
from menu import PSMenu
from dialogs import NewProcessDialog

class ProcessView():
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
            col.set_max_width(200)
            self.treeview.append_column(col)
            j += 1

        self.treeview.get_selection().connect("changed", self.on_selection)
        self.init_proc_list()

    def on_selection(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selected_pid = model[treeiter][0]

    def init_proc_list(self):
        thread = threading.Thread(target=self.populate_proc_list)
        thread.daemon = True
        thread.start()

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


class GnomePSWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gnome process explorer")
        self.set_default_size(200, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.process_view = ProcessView()
        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.set_vexpand(True)

        menu = PSMenu(self)
        self.menubar = menu.menubar

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.grid.attach(self.scrollable, 0, 1, 8, 10)

        self.scrollable.add(self.process_view.treeview)

        self.new_button = Gtk.Button("New Process")
        self.kill_button = Gtk.Button("Kill Process")
        self.new_button.connect("clicked", self.on_new_button_clicked)
        self.kill_button.connect("clicked", self.on_kill_button_clicked)

        self.grid.attach_next_to(self.new_button, self.scrollable,
                Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.kill_button, self.new_button,
                Gtk.PositionType.RIGHT, 1, 1)

        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.grid, True, True, 0)

        self.add(self.box)

        self.connect('delete-event', Gtk.main_quit)

        gobject.threads_init()
        self.show_all()
        Gtk.main()

    def on_new_button_clicked(self, button):
        dialog = NewProcessDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            procname = dialog.get_procname()
            os.system(procname)
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def on_kill_button_clicked(self, button):
        if self.process_view.selected_pid:
            try:
                os.kill(int(self.process_view.selected_pid), signal.SIGKILL)
                self.process_view.selected_pid = None
            except OSError:
                self.show_error("Error", "Could not kill process {0}".format(
                    self.process_view.selected_pid))

    def show_error(self, header="Error", text=""):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                 Gtk.ButtonsType.OK, header)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

win = GnomePSWindow()
