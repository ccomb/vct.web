from formalchemy.ext.zope import FieldSet
from repoze.bfg.chameleon_zpt import render_template_to_response, get_template
from repoze.bfg.security import remember, forget, authenticated_userid
from repoze.bfg.traversal import virtual_root, model_path
from repoze.bfg.url import model_url
from repoze.bfg.view import static
from security import USERS
from webob import Response
from webob.exc import HTTPFound
import models

static_view = static('templates/static')


def index_view(context, request):
    master = get_template('templates/master.pt')
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
           }


def patient_list(context, request):
    patients = context.values()
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patients':patients}


def patient_add(context, request):
    patient = models.Patient()
    form = FieldSet(models.IPatient)
    form.configure(exclude=[form.id])
    form.id.set(required=False)
    form = form.bind(patient, data=request.POST or None)
    if request.POST and form.validate():
        request.POST.pop('Patient--id', None)
        form.sync()
        id = len(context)
        while id in context:
            id += 1
        patient.id = str(id)
        context[str(id)] = patient
        catalog = virtual_root(context, request).catalogs['patients']
        catalog.index_doc(id, patient)
        return HTTPFound(location=model_url(patient, request))
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}

def patient_search(context, request):
    patient = models.Patient()
    form = FieldSet(models.IPatient)
    for field in form.render_fields:
        getattr(form, field).set(required=False)
    form = form.bind(patient, data=request.POST or None)
    catalog = virtual_root(context, request).catalogs['patients']
    number, results = None, {}
    if request.POST and form.validate():
        data = dict([(id,field.value)
                     for (id,field) in form.render_fields.items()
                     if field.value])
        number, results = catalog.search(**data) # XXX
        results = [context[i] for i in dict(results).keys()]
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form,
            'number': number,
            'results': results}




def patient_view(context, request):
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'context':context}



def patient_edit(context, request):
    form = FieldSet(models.IPatient)
    form = form.bind(context, data=request.POST or None)
    form.id.set(readonly=True)
    if request.POST and form.validate():
        request.POST.pop('Patient--id', None)
        form.sync()
        catalog = virtual_root(context, request).catalogs['patients']
        catalog.reindex_doc(int(context.id), context)
        return HTTPFound(location=model_url(context, request))
    return {'context': context,
            'request': request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}


def login(context, request):
    login_url = model_url(context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )


def logout(context, request):
    headers = forget(request)
    return HTTPFound(location = model_url(context, request),
                     headers = headers)









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




