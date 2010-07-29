from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid
from repoze.bfg.view import static

static_view = static('templates/static')


def index(context, request):
#    current_user = authenticated_userid(request)
#    user_organization = " Hospital XXX"   # should become the organization of the current user
    master = get_template('templates/master.pt')
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
#            'organization': user_organization,
           }


"""
def user_preferences(context, request):
    return {'request':request
        ,'context':context
        ,'master': get_template('templates/master.pt')
        ,'logged_in': authenticated_userid(request)
        }

"""


