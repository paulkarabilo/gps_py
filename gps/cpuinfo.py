from os import open

class CPU:
    def __init__(self, number):
        self.params = {"n": number}

    def set(self, param, value):
        self.params[param] = value

class CpuInfo:
    def __init__(self):
        self.cpus = {}

    def read(self):
        cur_proc = None
        with open("/proc/cpuinfo") as f:
            for l in f:
                [param, value] = l.split(':')
                param = param.strip()
                name = name.strip()
                if param is "processor":
                    self.cpus[value] = CPU(value) if value not in self.cpus else self.cpus[value]
                    cur_proc = value
                else:
                    self.cpus[cur_proc].set(param, value)