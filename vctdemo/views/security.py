from repoze.bfg.security import remember, forget
from repoze.bfg.url import model_url
from repoze.bfg.view import static
from vctdemo.security import USERS
from webob.exc import HTTPFound

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

