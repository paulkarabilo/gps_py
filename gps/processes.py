"""
    Processes module
"""

import psutil
from gps.usersgroups import UsersGroups

class ProcessList:
    names = ['pid', 'name', 'status']
    types = [int, str, str]

    def __init__(self):
        self.processes = []
        self.sort_column = 'pid'
        self.sort_reverse = False
        self.usersgroups = UsersGroups()

    def read(self):
        self.processes = []
        for p in psutil.process_iter():
            self.processes.append({
                'pid': p.pid,
                'status': p.status(),
                'name': p.name()
            })
        self.sort()

    def sort(self):
        if self.sort_column == 'pid':
            self.processes.sort(key=lambda proc: proc["pid"], reverse=self.sort_reverse)
        else:
            index = self.names.index(self.sort_column)
            t = self.types[index]
            if t is str:
                self.processes.sort(key=lambda proc: proc[self.sort_column].lower(),
                                reverse=self.sort_reverse)
            else:
                self.processes.sort(key=lambda proc: proc[self.sort_column],
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

