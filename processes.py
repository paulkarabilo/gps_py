import os


class Process:
    def __init__(self, pid, cmdline, status):
        self.pid = pid
        self.cmdline = cmdline
        self.status = status
        self.status_codes = {}
        for row in self.status.split('\n'):
            cols = row.split(':')
            if len(cols) == 2:
                [name, value] = cols
                self.status_codes[name.strip()] = value.strip()

    def get_status(self, code):
        return self.status_codes[code] or ""


class ProcessList:
    names = ['Name', 'Pid', 'Uid', 'Gid']
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

    def get_proc_stats(self):
        return self.names
        if len(self.processes) is 0:
            self.read()
        keys = []
        for pid in self.processes:
            for key in self.processes[pid].status_codes:
                if not key in keys:
                    keys.append(key)
        return keys

    def get(self, pid):
        return self.processes[pid]


if __name__ == "__main__":
    pl = ProcessList()
    print len(pl.processes)
    print pl.get_proc_stats()
