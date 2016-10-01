from os import open

class CPU:
    def __init__(self):
        pass


class CpuInfo:
    def __init__(self):
        self.cpus = {}

    def read(self):
        with open("/proc/cpuinfo") as f:
            for l in f:
                print l
