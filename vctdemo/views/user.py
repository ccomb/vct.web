from formalchemy.ext.zope import FieldSet
from formalchemy.fields import PasswordFieldRenderer
from pyramid.chameleon_zpt import get_template
from vctdemo.models import IUserPreferences
from pyramid.security import authenticated_userid
from pyramid.traversal import virtual_root
from pyramid.url import model_url
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from vctdemo import models
from webob.exc import HTTPFound
import xmlrpclib

def listview(context, request):
    users = context.values()
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'users':users}


def add(context, request):
    server = xmlrpclib.ServerProxy('http://localhost:8000')
    form = server.get_form('user', 'html')
    template = 'user_add_test.pt'

    if request.POST:
        data = [ i for i in request.POST.items() if i[1]!='']
        server = xmlrpclib.ServerProxy('http://localhost:8000')
        import random
        response = server.put('frsecu', random.randint(0,10000), data, 'user')
        if response is not 0:
            form = server.get_form('user', 'html', data)
        else:
            return HTTPFound(location=next_page)
            
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}

def view(context, request):
    user_organization = "St Peter Hospital" #authenticated_userid.organization
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'context':context}


def edit(context, request):
    form = FieldSet(models.IUser)
    form = form.bind(context, data=request.POST or None)
    form.username.set(readonly=True)
    form.password.set(renderer=PasswordFieldRenderer)
    if request.POST and form.validate():
        form.sync()
        return HTTPFound(location=model_url(context, request))
    return {'context': context,
            'request': request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}


def preferences(context, request):
    form = FieldSet(models.IUserPreferences)
    preferences = IUserPreferences(context)
    #form.username.set(readonly=True)
    form = form.bind(preferences, data=request.POST or None)
    if request.POST and form.validate():
        form.sync()
        return HTTPFound(location=model_url(context, request))
    return {'request':request,
            'context':context,
            'form': form,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            }


def my_preferences(context, request):
    """view for my preferences
    """
    return preferences(context[authenticated_userid(request)], request)


def user_admin_menu(context, request):
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            }

def user_patient_groups(context, request):
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            }
def user_test(context, request):
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            }
def user_todo(context, request):
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            }




