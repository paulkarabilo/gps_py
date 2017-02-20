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
        self.sort_column = 'pid'
        self.sort_reverse = False
        self.usersgroups = UsersGroups()

    def read(self):
        self.processes = {}
        for p in psutil.process_iter():
            self.processes[p.pid] = {
                'pid': p.pid,
                'status': p.status(),
                'name': p.name()
            }

    def sort(self, processes):
        index = self.names.index(self.sort_column)
        t = self.types[index]
        if t is str:
            processes.sort(key=lambda proc: proc[self.sort_column].lower(),
                            reverse=self.sort_reverse)
        else:
            processes.sort(key=lambda proc: proc[self.sort_column],
                            reverse=self.sort_reverse)
        return processes

    def list(self):
        return self.sort([v for v in self.processes.values()])

    def get_proc_stats(self):
        return self.names

    def get_proc_types(self):
        return self.types

    def get(self, pid):
        return self.processes[pid]

    def sort_by(self, column):
        if column not in self.names:
            return None
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
        return self.sort_reverse

