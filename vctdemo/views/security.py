from persistent.list import PersistentList
from pkg_resources import get_distribution
from pyramid.security import remember, forget
from pyramid.traversal import virtual_root
from pyramid.url import model_url
from pyramid.view import static
from vctdemo import views
from vctdemo.models import User
from vctdemo.security import GROUPS
from webob import Response
from webob.exc import HTTPFound

def login(context, request):
    # get the url of the login page
    login_url = model_url(context, request, 'login')
    referrer = request.url
    # don't redirect from the login page to itself
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']

        # read the user folder
        server = xmlrpclib.ServerProxy('http://localhost:8000')
        response = server.login(login, password)
        if not response:
            message = 'Failed login'
        else:
            token = response
            headers = remember(request, token)
            return HTTPFound(location = came_from,
                             headers = headers)
        
    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        version = get_distribution('vct.demo').version,
        login = login,
        password = '',
        )


def logout(context, request):
    headers = forget(request)
    # redirect to the context
    return HTTPFound(location = model_url(context, request),
                     headers = headers)

