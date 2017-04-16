from gi.repository import Gtk, Gio
from views.window import GnomePSWindow


class Application(Gtk.Application):
    def __init__(self, argv):
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.GnomePS",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self._window = None

    def do_activate(self):
        if not self._window:
            self._window = GnomePSWindow(self)
        self._window.present()
