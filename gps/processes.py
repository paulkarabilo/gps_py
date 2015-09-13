import os
import re
from usersgroups import UsersGroups


class Process:
    def __init__(self, pid, cmdline, status, usersgroups):
        self.pid = pid
        self.cmdline = cmdline
        self.status = status
        self.status_codes = {}
        for row in self.status.split('\n'):
            cols = row.split(':')
            if len(cols) == 2:
                [name, value] = cols
                self.status_codes[name.strip()] = value.strip()
        if 'Uid' in self.status_codes:
            self.parse_uid(usersgroups)
        if 'Gid' in self.status_codes:
            self.parse_gid(usersgroups)

    def parse_uid(self, usersgroups):
        uids = set(re.split(r'\t+', self.status_codes['Uid']))
        users = []
        for u in uids:
            users.append(usersgroups.get_username(u))
        self.status_codes['Users'] = '||'.join(users)

    def parse_gid(self, usersgroups):
        gids = set(re.split(r'\t+', self.status_codes['Gid']))
        groups = []
        for g in gids:
            groups.append(usersgroups.get_groupname(g))
        self.status_codes['Groups'] = '||'.join(groups)

    def get_status(self, code):
        return self.status_codes[code] or ""


class ProcessList:
    names = ['Pid', 'Name', 'Users', 'Groups', 'State']

    def __init__(self):
        self.processes = {}
        self.usersgroups = UsersGroups()

    def read(self):
        self.processes = {}
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
                self.processes[pid] = Process(int(pid), cmdline, status, self.usersgroups)

    def list(self):
        print(len(self.processes))
        for pid in self.processes:
            yield self.processes[pid]

    def get_proc_stats(self):
        return self.names

    def get(self, pid):
        return self.processes[pid]


if __name__ == "__main__":
    pl = ProcessList()
    print len(pl.processes)
    print pl.get_proc_stats()
