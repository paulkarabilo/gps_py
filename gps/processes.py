from os import path, listdir
import re
from usersgroups import UsersGroups
import multiprocessing

_scale = {'kB': 1024, 'mB': 1024*1024,
          'KB': 1024, 'MB': 1024*1024}


class Process:
    def __repr__(self):
        return "<Proc>"

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
        if 'VmSize' in self.status_codes:
            self.parse_mem('VmSize', 'Memory, kB')
        if 'VmRSS' in self.status_codes:
            self.parse_mem('VmSize', 'Resident Memory, kB')
        if 'VmStk' in self.status_codes:
            self.parse_mem('VmStk', 'Stack, kB')

    def parse_mem(self, source, target):
        mem = self.status_codes[source].split(None, 3)
        self.status_codes[target] = int(mem[0]) * _scale[mem[1]] / 1024

    def parse_uid(self, usersgroups):
        users = []
        for u in set(re.split(r'\t+', self.status_codes['Uid'])):
            users.append(usersgroups.get_username(u))
        self.status_codes['Users'] = '||'.join(users)

    def parse_gid(self, usersgroups):
        groups = []
        for g in set(re.split(r'\t+', self.status_codes['Gid'])):
            groups.append(usersgroups.get_groupname(g))
        self.status_codes['Groups'] = '||'.join(groups)

    def get_status(self, code):
        return self.status_codes[code] or ""


def try_read_proc(params):
    try:
        cmdline = open(path.join('/proc', params["pid"], 'cmdline'), 'rb').read()
        status = open(path.join('/proc', params["pid"], 'status'), 'rb').read()
    except IOError:
        return None
    if cmdline:
        return Process(int(params["pid"]), cmdline, status, params["usersgroups"])


class ProcessList:
    names = ['Pid', 'Name', 'Users', 'Groups', 'State', 'Memory, kB', 'Resident Memory, kB', 'Stack, kB']
    types = [str, str, str, str, str, int, int, int]

    def __init__(self):
        self.processes = []
        self.sort_column = 'Pid'
        self.sort_reverse = False
        self.usersgroups = UsersGroups()

    def read(self):
        self.processes = filter(
            None,
            multiprocessing.Pool(processes=8).map(
                try_read_proc,
                [{'pid': pid, 'usersgroups': self.usersgroups}
                 for pid in listdir('/proc')
                 if pid.isdigit()]
            )
        )
        self.sort()

    def sort(self):
        if self.sort_column == 'Pid':
            self.processes.sort(key=lambda proc: proc.pid, reverse=self.sort_reverse)
        else:
            index = self.names.index(self.sort_column)
            t = self.types[index]
            if t is str:
                self.processes.sort(key=lambda proc: proc.get_status(self.sort_column).lower(),
                                reverse=self.sort_reverse)
            else:
                self.processes.sort(key=lambda proc: proc.get_status(self.sort_column),
                                reverse=self.sort_reverse)

    def list(self):
        return self.processes

    def get_proc_stats(self):
        return self.names

    def get_proc_types(self):
        return self.types

    def get(self, pid):
        return self.processes[pid]

    def sort_by(self, column):
        if column not in self.names:
            return
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
        return self.sort_column, self.sort_reverse

