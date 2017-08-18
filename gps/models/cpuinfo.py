import psutil

class CpuInfo:
    def __init__(self):
        self.cpus = {}

    def read(self):
        self.cpus = {}

        