from os import open

class MemInfo:
    def __init__(self):
        self.info = {}

    def read(self):
        with open("/proc/meminfo") as f:
            for l in f:
                [name, value] = l.split(':')
                self.info[name.strip()] = value.strip()
