USERS = {
        'admin': 'pass2',
        'test' :'test',
        }

GROUPS = {
          'admin':['group:admins'],
          'test' :['group:admins'],
          'toto' :['group:admins'],
         }

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

