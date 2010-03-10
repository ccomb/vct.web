from formalchemy.ext.zope import FieldSet
from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.url import model_url
from repoze.bfg.view import static
from webob import Response
from webob.exc import HTTPFound
import models

static_view = static('templates/static')


def index_view(context, request):
    return {'request':request, 'context':context}


def patient_list(context, request):
    patients = context.values()
    return {'request':request,
            'context':context,
            'patients':patients}


def patient_add(context, request):
    name = None
    if 'name' in request.params:
        name = request.params['name']
        id = len(context)
        while id in context:
            id += 1
        id = str(id)
        patient = models.Patient()
        patient.id = id
        patient.name = name
        context[str(id)] = patient
    return {'request':request,
            'context':context}

def patient_view(context, request):
    return {'request':request,
            'context':context}

PatientEditForm = FieldSet(models.IPatient)


def patient_edit(context, request):
    form = PatientEditForm.bind(context, data=request.POST or None)
    form.id.set(readonly=True)
    if request.POST and form.validate():
        request.POST.pop('Patient--id', None)
        form.sync()
        return HTTPFound(location=model_url(context, request))
    return {'context': context,
            'request': request,
            'form': form}



def test_view(context, request):
    return {'request':request, 'context':context}

def user_authentication(context, request):
    user_ID= request.params.get('user_ID')
    print "user_ID = " + user_ID
    password = request.params.get('user_password')
    if password == "test":
        return HTTPFound(location= "/patients_old/user_session")
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




