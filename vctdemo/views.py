from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.view import static
from webob import Response
from webob.exc import HTTPFound

static_view = static('templates/static')


def index_view(context, request):
    return {'request':request, 'context':context}

def test_view(context, request):
    return {'request':request, 'context':context}

def user_authentication(context, request):
    user_ID= request.params.get('user_ID')
    print "user_ID = " + user_ID
    password = request.params.get('user_password')
    if password == "test":
        return HTTPFound(location= "/patients/user_session")
    else:
        return HTTPFound(location= "/")

def user_session(context, request):
    return {'request':request, 'context':context}

def patient_search(context, request):
    return {'request':request, 'context':context}

def patient_groups(context, request):
    return {'request':request, 'context':context}

def patient_group(context, request):
    return {'request':request, 'context':context}

def patient_ID_validation(context, request):
    return {'request':request, 'context':context}

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
    return {'request':request, 'context':context}

def BFG_main_page(context, request):
    return {'request':request, 'context':context}

def patient_add(context, request):
    return {'request':request,
            'context':context }


class PatientList(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return {'request':self.request,
                'context':self.context}


def patient_edit(context, request):
    return Response(u'patient edit')


def patient_view(context, request):
    return render_template_to_response("templates/patient.pt",
        request = request,
        project = 'vct.demo')

    #return("templates/static/Help/Notifications-Help.html")

