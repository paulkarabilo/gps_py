import os

class Process:
    def __init__(self, pid, cmdline, status):
        self.pid = pid
        self.cmdline = cmdline
        self.status = status

class ProcessList:
    def __init__(self):
        self.processes = {}

    def read(self):
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            try:
                cmdline = open(os.path.join('/proc', pid, 'cmdline'),
                        'rb').read()
                status = open(os.path.join('/proc', pid, 'status'),
                        'rb').read()
            except IOError:
                continue

            if cmdline:
                self.processes[pid] = Process(pid, cmdline, status)

    def list(self):
        for pid in self.processes:
            yield self.processes[pid]

    def get(self, pid):
        return self.processes[pid]
