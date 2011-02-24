from os.path import dirname, join
from pyramid.chameleon_zpt import render_template_to_response, get_template
from pyramid.security import authenticated_userid

def help_view(context, request):
    subpath = '/'.join(['templates', 'help'] + list(request.subpath))
    return render_template_to_response(subpath,
                                       request=request,
                                       logged_in=authenticated_userid(request),
                                       master=get_template('templates/master.pt'))

