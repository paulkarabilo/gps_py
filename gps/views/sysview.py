from gps.models.meminfo import MemInfo
from gps.models.cpuinfo import CpuInfo

class SystemView:
    def __init__(self, window):
        self.window = window
        self.cpuinfo = CpuInfo()
        self.meminfo = MemInfo()

    def update(self):
        pass
    
    def destroy(self):
        pass
