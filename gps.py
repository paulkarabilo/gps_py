from gi.repository import Gtk, Gdk, GLib

import gobject
import os
import signal
import time
import threading

from processes import ProcessList


class NewProcessDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Start new process", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        self.entry = Gtk.Entry()
        self.get_content_area().add(self.entry)
        self.show_all()

    def get_procname(self):
        return self.entry.get_text()


class PSThread(threading.Thread):
    def __init__(self, callback):
        self.callback = callback
        self.stopped = False
        threading.Thread.__init__(self)

    def run(self):
        while not self.stopped:
            self.callback()
            time.sleep(1)


class ProcessView():
    columns = [("PID", str), ("Path", str)]

    def __init__(self):
        self.first_init = False
        self.processes = ProcessList()
        self.liststore = Gtk.ListStore(int, str)
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
        self.processes.read()
        if not self.first_init:
            self.liststore.clear()
            for proc in self.processes.list():
                self.liststore.append([proc.pid, proc.cmdline])
            self.first_init = True
        else:
            iter = 0
            for proc in self.processes.list():
                self.liststore[iter] = [proc.pid, proc.cmdline]
                iter += 1

        gobject.timeout_add(2000, self.populate_proc_list)


class GnomePSWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gnome process explorer")
        self.set_border_width(10)
        self.set_default_size(200, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.process_view = ProcessView()
        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.set_vexpand(True)

        self.grid.attach(self.scrollable, 0, 0, 8, 10)

        self.scrollable.add(self.process_view.treeview)

        self.new_button = Gtk.Button("New Process")
        self.kill_button = Gtk.Button("Kill Process")
        self.new_button.connect("clicked", self.on_new_button_clicked)
        self.kill_button.connect("clicked", self.on_kill_button_clicked)

        self.grid.attach_next_to(self.new_button, self.scrollable,
                Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.kill_button, self.new_button,
                Gtk.PositionType.RIGHT, 1, 1)

        self.add(self.grid)

        self.show_all()

        self.connect('delete-event', Gtk.main_quit)

        gobject.threads_init()
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
