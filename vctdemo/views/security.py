from repoze.bfg.security import remember, forget
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.bfg.view import static
from webob.exc import HTTPFound
from vctdemo.security import FAILSAFE_PASS

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

        # try the failsafe admin first (see ../security.py)
        if FAILSAFE_PASS != '' and [login, password] == ['admin', FAILSAFE_PASS]:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)

        # read the user folder
        users = virtual_root(context, request)['users']
        user = users.get(login, None)
        if user is not None and user.password == password:
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

