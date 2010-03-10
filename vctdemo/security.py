USERS = {'admin': 'pass', 'test':'test'}

GROUPS = {'admin':['group.admins']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

