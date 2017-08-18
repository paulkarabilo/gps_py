from gps.models.system import SystemInfo

class SystemView:
    def __init__(self, window):
        self.meminfo = SystemInfo()
        self.window = window