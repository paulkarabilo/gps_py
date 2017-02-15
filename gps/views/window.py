from gi.repository import Gtk, GObject

import os
import time
import signal

from menu import PSMenu
from dialogs import NewProcessDialog
from procview import ProcessView

class GnomePSWindow(Gtk.Window):
    def __init__(self, app):
        Gtk.Window.__init__(self,
                            title="Gnome process explorer",
                            application=app)

        self.active_tab = None
        self.timeout_id = None
        self.set_default_size(200, 200)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.set_vexpand(True)

        menu = PSMenu(self)
        self.menubar = menu.menubar

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.grid.attach(self.scrollable, 0, 1, 8, 10)

        self.show_processes()

        self.grid.set_border_width(5)
        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.grid, True, True, 0)

        self.add(self.box)

        self.connect('delete-event', Gtk.main_quit)

        self.show_all()
        self.update_view()

    def show_processes(self):
        if not isinstance(self.active_tab, ProcessView):
            if self.active_tab != None:
                self.active_tab.destroy()
            self.active_tab = ProcessView(self)
            self.scrollable.add(self.active_tab.treeview)

    def show_network(self):
        pass

    def show_stats(self):
        pass

    def on_new_button_clicked(self, button):
        dialog = NewProcessDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            procname = dialog.get_procname()
            if not procname.endswith(' &'):
                procname += ' &'
            os.system(procname)
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def on_kill_button_clicked(self, button):
        if isinstance(self.active_tab, ProcessView):
            self.active_tab.kill_process(0)

    def show_error(self, header="Error", text=""):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK, header)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()


    def update_view(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.active_tab.update()
        self.timeout_id = GObject.timeout_add(2000, self.update_view)
