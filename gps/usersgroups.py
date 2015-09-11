import pwd
import grp


class UsersGroups:
    def __init__(self):
        self.groups = {}
        for g in grp.getgrall():
            self.groups[g.gr_gid] = {'name': g.gr_name}
        self.users = {}
        for p in pwd.getpwall():
            self.users[p.pw_uid] = {'name': p.pw_name,
                                    'group': self.groups[p.pw_gid]['name']}

    def get_username(self, uid):
        id = int(uid)
        if id in self.users:
            return self.users[int(id)]['name']
        else:
            return ''

    def get_usergroupname(self, uid):
        id = int(uid)
        if id in self.users:
            return self.users[id]['group']
        else:
            return ''

    def get_groupname(self, gid):
        id = int(gid)
        if id in self.groups:
            return self.groups[id]['name']
        else:
            return ''
