from persistent.list import PersistentList
from pkg_resources import get_distribution
from repoze.bfg.security import remember, forget
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.bfg.view import static
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

    users = virtual_root(context, request)['users']
    if len(users) == 0:
        if 'username' in request.params:
            username = request.params.get('username')
            password = request.params.get('password')
            if password != request.params.get('confirm'):
                message = u'Passwords differ!'
            elif password == u'' or username == u'':
                message = u'Please enter a username and password'
            else:
                user = User()
                user.username = username
                user.password = password
                user.groups = PersistentList(GROUPS)
                users[username] = user
                return HTTPFound(location = '/')

        return Response("""
        <html><body><span style="color: red">%s</span><br/>
        Please create the initial administrator:<br/>
        <form method="POST" action="">
        username: <input type="text" name="username"/><br/>
        password: <input type="password" name="password"/><br/>
        confirm password: <input type="password" name="confirm"/><br/>
        <input type="submit" />
        </form></body></html>
        """ % message)

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']

        # read the user folder
        user = users.get(login, None)
        if user is not None and user.password == password:
            # shortcut for storing the logged-in user in the session
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)

        message = 'Failed login'

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

