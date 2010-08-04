from formalchemy.ext.zope import FieldSet
from formalchemy.fields import PasswordFieldRenderer
from repoze.bfg.chameleon_zpt import get_template
from vctdemo.models import IUserPreferences
from repoze.bfg.security import authenticated_userid
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from vctdemo import models
from webob.exc import HTTPFound

def listview(context, request):
    users = context.values()
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'users':users}


def add(context, request):
    user = models.User()
    form = FieldSet(models.IUser)
    form.password.set(renderer=PasswordFieldRenderer)
    form = form.bind(user, data=request.POST if len(request.POST) else request.GET or None)  #???
    if request.POST and form.validate():
        form.sync()
        context[user.username] = user
        return HTTPFound(location=model_url(user, request) + '/@@prefs')
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




