from os.path import dirname, join, exists
from os import getcwd
from repoze.bfg.traversal import virtual_root

GROUPS = ['group:admins', 'group:users', 'group:patients']

def groupfinder(userid, request):
    if userid == 'admin':
        return GROUPS
    user = virtual_root(None, request)['users'].get(userid, None)
    if user is not None:
        return user.groups
    return []


# check if we have a failsafe file with user:pass
FAILSAFE_PASS = ''
_failsafe_path =  join(getcwd, dirname(__file__), 'admin')
if exists(_failsafe_path):
    with open(_failsafe_path) as f:
        FAILSAFE_PASS = f.read().strip()
