from gi.repository import Gtk

import gobject
import os
import signal

from menu import PSMenu
from dialogs import NewProcessDialog
from procview import ProcessView


class GnomePSWindow(Gtk.Window):
    def __init__(self, app):
        Gtk.Window.__init__(self,
                            title="Gnome process explorer",
                            application=app)

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

        self.kill_button.set_border_width(5)
        self.new_button.set_border_width(5)

        self.grid.attach_next_to(self.new_button, self.scrollable,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.kill_button, self.new_button,
                                 Gtk.PositionType.RIGHT, 1, 1)

        self.grid.set_border_width(5)
        self.box.pack_start(self.menubar, False, False, 0)
        self.box.pack_start(self.grid, True, True, 0)

        self.add(self.box)

        self.connect('delete-event', Gtk.main_quit)

        gobject.threads_init()
        self.show_all()

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
