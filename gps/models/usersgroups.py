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
        return self.users[id]['name'] if id in self.users else ''

    def get_usergroupname(self, uid):
        id = int(uid)
        return self.users[id]['group'] if id in self.users else ''

    def get_groupname(self, gid):
        id = int(gid)
        return self.groups[id]['name'] if id in self.groups else ''
