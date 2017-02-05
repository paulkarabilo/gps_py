"""
    Processes module
"""

import re
import multiprocessing
import psutil
from os import path, listdir

from .usersgroups import UsersGroups



_scale = {'kB': 1024, 'mB': 1024*1024,
          'KB': 1024, 'MB': 1024*1024}


class Process:
    def __repr__(self):
        return "<Proc>"

    def __init__(self, attrs):
        self.attrs = attrs

    def get_attr(self, attr):
        return self.attrs[attr] or ""


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
            self.processes.append(Process(p.as_dict()))
        self.sort()

    def sort(self):
        if self.sort_column == 'pid':
            self.processes.sort(key=lambda proc: proc.get_attr("pid"), reverse=self.sort_reverse)
        else:
            index = self.names.index(self.sort_column)
            t = self.types[index]
            if t is str:
                self.processes.sort(key=lambda proc: proc.get_attr(self.sort_column).lower(),
                                reverse=self.sort_reverse)
            else:
                self.processes.sort(key=lambda proc: proc.get_attr(self.sort_column),
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

