import gtk

class GPSApp(gtk.Window):
    def __init__(self):
        super(GPSApp, self).__init__()

        self.connect("destroy", gtk.main_quit)
        self.set_size_request(250, 150)
        self.set_position(gtk.WIN_POS_CENTER)
        self.show()


GPSApp()
gtk.main()
