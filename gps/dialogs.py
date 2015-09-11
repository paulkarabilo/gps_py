from gi.repository import Gtk


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