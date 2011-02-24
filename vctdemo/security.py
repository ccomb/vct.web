from os.path import dirname, join, exists
from os import getcwd
from pyramid.traversal import virtual_root

GROUPS = ['group:admins', 'group:users', 'group:patients', 'group:test']

def groupfinder(userid, request):
    user = virtual_root(None, request)['users'].get(userid, None)
    if user is not None:
        return user.groups
    return []

