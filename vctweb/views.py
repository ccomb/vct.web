import xmlrpclib, urllib
from pyramid.chameleon_zpt import get_template
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from webob.exc import HTTPFound
from pyramid.view import render_view
from pyramid.renderers import render as render_template


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
    server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
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



def patient_items(request):
    server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
    patient_id = request.matchdict['id']
    nb, results = server.get_by_uid('local', patient_id, 'patient')
    patient = results[0]['data']
    items_ids = patient.get('items')
    items = []
    items_html = []
    if items_ids is not None:
        items = server.get_by_uids('local', items_ids, 'observation')
    for item in items[1]:
        items_html.append(render_template('templates/patient_item_smallview.pt', item['data'], request))

    return {'request':request,
            'master': get_template('templates/master.pt'),
            'patient_master': get_template('templates/patient_master.pt'),
            'logged_in': authenticated_userid(request),
            'errors': None,
            'patient': results[0]['data'],
            'patient_url': route_url('patient_view', request, id=patient_id),
            'items': items,
            'items_html': items_html,
            'render_template': render_template,
            }


def patient_item_add(request):
    server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
    # get the patient
    patient_id = request.matchdict['id']
    nb, results = server.get_by_uid('local', patient_id, 'patient')
    patient = results[0]['data']
    # get the item type to create
    item_type = request.GET['type']
    # add the item
    if request.POST:
        item = dict(request.POST)
        item['patient'] = patient_id
        response = server.put('', '', item, item_type)
        if type(response) is not str or not response.isdigit():
            data = [ (i,j) for (i,j) in request.POST.items() if j!='']
            form = server.get_form(item_type, 'html', True, data)
        else:
            # add the item in patient
            if 'items' not in patient:
                patient['items'] = []
            patient['items'].append(response)
            response = server.put('local', patient_id, patient, 'patient')
            return HTTPFound(location='./items')
    # display the form
    else:
        data = request.POST if len(request.POST) else request.GET
        form = server.get_form(item_type, 'html', False, data.items())

    return {'request':request,
            'master': get_template('templates/master.pt'),
            'patient_master': get_template('templates/patient_master.pt'),
            'patient': results[0]['data'],
            'patient_url': route_url('patient_view', request, id=patient_id),
            'item_type': item_type,
            'logged_in': authenticated_userid(request),
            'errors': None,
            'form': form,
            }


def patient_add(request):
    form = None
    server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
    if request.POST:
        response = server.put('', '', dict(request.POST), 'patient')
        if type(response) is not str or not response.isdigit():
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


def patient_edit(request):
    patient_id = request.matchdict['id']
    server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
    if request.POST:
        response = server.put('', '', dict(request.POST), 'patient')
        if type(response) is not str or not response.isdigit():
            data = [ (i,j) for (i,j) in request.POST.items() if j!='']
        else:
            return HTTPFound(location='.')
    else:
        nb, results = server.get_by_uid('local', patient_id, 'patient')
        form = server.get_form('patient', 'html', True, results[0]['data'].items())
    patient = results[0]['data']

    return {'request':request,
            'master': get_template('templates/master.pt'),
            'patient_master': get_template('templates/patient_master.pt'),
            'logged_in': authenticated_userid(request),
            'patient': patient,
            'patient_url': route_url('patient_view', request, id=patient_id),
            'errors': None,
            'form': form,
            }


def patient_view(request):
    patient_id = request.matchdict['id']
    server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
    nb, results = server.get_by_uid('local', patient_id, 'patient')
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'patient_master': get_template('templates/patient_master.pt'),
            'logged_in': authenticated_userid(request),
            'errors': None,
            'patient': results[0]['data'],
            'patient_url': route_url('patient_view', request, id=patient_id),
            }



