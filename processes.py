import os


class Process:
    def __init__(self, pid, cmdline, status):
        self.pid = pid
        self.cmdline = cmdline
        self.status = status
        self.status_codes = {}
        for row in self.status.split('\n'):
            (name, value) = row.split(':')
            self.status_codes[name.strip()] = value.strip()


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
                self.processes[pid] = Process(int(pid), cmdline, status)

    def list(self):
        print(len(self.processes))
        for pid in self.processes:
            yield self.processes[pid]

    def get(self, pid):
        return self.processes[pid]


if __name__ == "__main__":
    pl = ProcessList()
    pl.read()
    pl.processes[0].