import gi
gi.require_version('Gtk', '3.0')

from gps.application import Application
from signal import signal, SIG_DFL, SIGINT
import sys

if __name__ == "__main__":
    app = Application(sys.argv)
    signal(SIGINT, SIG_DFL)
    status = app.run()
    sys.exit(status)
