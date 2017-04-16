"""
    Processes module
"""

import psutil
from gps.models.usersgroups import UsersGroups

class ProcessList:
    names = ['pid', 'name', 'status']
    types = [int, str, str]

    def __init__(self):
        self.processes = []
        self.usersgroups = UsersGroups()

    def read(self):
        self.processes = {}
        for p in psutil.process_iter():
            self.processes[p.pid] = {
                'pid': p.pid,
                'status': p.status(),
                'name': p.name()
            }

    def list(self):
        return self.processes.values()

    def get_proc_stats(self):
        return self.names

    def get_proc_types(self):
        return self.types

    def get(self, pid):
        return self.processes[pid]
