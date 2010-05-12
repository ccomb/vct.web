from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid
from repoze.bfg.view import static

static_view = static('templates/static')


def index(context, request):
    master = get_template('templates/master.pt')
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
           }




def test_view(context, request):
    return {'request':request
        ,'context':context
        ,'master': get_template('templates/master.pt')
        ,'logged_in': authenticated_userid(request)
        }

def patient_groups(context, request):
    return {'request':request, 
        'context':context,
        'master': get_template('templates/master.pt'),
        'logged_in': authenticated_userid(request),
        }

def patient_group(context, request):
    return {'request':request,
        'context':context,
        'master': get_template('templates/master.pt'),
        'logged_in': authenticated_userid(request)
        }

def current_patient(context, request):
    return {'request':request, 'context':context}

def patient_menu(context, request):
    return {'request':request, 'context':context}

def event_list(context, request):
    return {'request':request, 'context':context}

def topics(context, request):
    return {'request':request, 'context':context}

def problem_list(context, request):
    return {'request':request, 'context':context}

def care_plan(context, request):
    return {'request':request, 'context':context}

def care_team(context, request):
    return {'request':request, 'context':context}

def patient_administration(context, request):
    return {'request':request, 'context':context}

def medData_template(context, request):
    return {'request':request, 'context':context}

def todo_help(context, request):
    return {'request':request, 'context':context}

def notification_help(context, request):
    return {'request':request, 'context':context}

def user_preferences(context, request):
    return {'request':request
        ,'context':context
        ,'master': get_template('templates/master.pt')
        ,'logged_in': authenticated_userid(request)
        }




