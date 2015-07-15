from gi.repository import Gtk

from processes import ProcessList

class GnomePSWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererText Example")

        self.set_default_size(200, 200)
        self.processes = ProcessList()
        self.processes.read()

        self.liststore = Gtk.ListStore(str, str)
        for proc in self.processes.list():
            print "{0} {1}".format(proc.pid, proc.cmdline)
            self.liststore.append([proc.pid, proc.cmdline])

        treeview = Gtk.TreeView(model=self.liststore)

        pid_text = Gtk.CellRendererText()
        pid_col = Gtk.TreeViewColumn("PID", pid_text, text=0)
        pid_col.set_max_width(300)
        treeview.append_column(pid_col)

        path_text = Gtk.CellRendererText()
        path_col = Gtk.TreeViewColumn("Path", path_text, text=1)
        path_col.set_max_width(300)
        treeview.append_column(path_col)

        self.add(treeview)



win = GnomePSWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
