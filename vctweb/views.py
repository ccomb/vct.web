import xmlrpclib, urllib
from pyramid.chameleon_zpt import get_template
from pyramid.security import authenticated_userid
from webob.exc import HTTPFound


def my_view(request):
    return {'project':'vct.web'}


def home(request):
    """view for the home page
    """
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request)
            }

def patients(request):
    """patients search and list
    """
    server = xmlrpclib.ServerProxy('http://localhost:8000')
    number = searched = patients = add_data = None

    if request.POST and 'Search' in request.POST:
        data = dict([ i for i in request.POST.items() if i[1]!=''])
        data.pop('Search')
        add_data = urllib.urlencode(data)
        searched = True
        number, patients = server.get_by_data(data, 'patient')

    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'errors': None,
            'number': number,
            'patients': patients,
            'searched': searched,
            'add_data': add_data,
            }


def patient_add(request):
    form = None
    server = xmlrpclib.ServerProxy('http://localhost:8000')
    if request.POST:
        response = server.put('', '', dict(request.POST), 'patient')
        if not response.isdigit():
            data = [ (i,j) for (i,j) in request.POST.items() if j!='']
            form = server.get_form('patient', 'html', True, data)
        else:
            return HTTPFound(location='.')

    else:
        data = request.POST if len(request.POST) else request.GET
        form = server.get_form('patient', 'html', False, data.items())

    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'errors': None,
            'form': form,
            }


def patient_view(request):
    raise NotImplementedError # use server.get_by_uid()



