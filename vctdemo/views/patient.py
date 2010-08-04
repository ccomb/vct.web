from formalchemy.ext.zope import FieldSet
from os.path import join
from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.bfg.view import static
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from vctdemo import models
from vctdemo.models import IRelations
from webob.exc import HTTPFound
import urllib

def listview(context, request):
    """patient list (in the context of patient container)
    """
    patients = context.values()
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patients':patients}


def add(context, request):
    # create a patient
    patient = models.Patient()
    form = FieldSet(models.IPatient)
    form.configure(exclude=[form.id])
    form.id.set(required=False)
    # bind form data to the patient.
    # if we have data coming from the search form, get them via GET
    form = form.bind(patient,
                     data=request.POST if len(request.POST) else request.GET)
    # if the form is submitted and validated
    if request.POST and form.validate():
        # don't use the id from the form
        request.POST.pop('Patient--id', None)
        # write the patient attributes from the form
        form.sync()
        # then choose and write the id
        id = len(context)
        while id in context:
            id += 1
        patient.id = str(id)
        context[str(id)] = patient
        catalog = virtual_root(context, request).catalogs['patients']
        catalog.index_doc(id, patient)
        # create a catalog for the items if there is none
        patient.catalogs = Folder()
        if 'items' not in patient.catalogs:
            patient.catalogs['items'] = Catalog()
            patient.catalogs['items']['title'] = CatalogTextIndex('title')
            patient.catalogs['items']['text'] = CatalogTextIndex('text')
        return HTTPFound(location=model_url(patient, request))

    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}

def search(context, request):
    patient = models.Patient()
    form = FieldSet(models.IPatient)
    # On which fiels to search ?
    for field in form.render_fields:
        getattr(form, field).set(required=False)
    form = form.bind(patient, data=request.POST or None)
    catalog = virtual_root(context, request).catalogs['patients']

    #print "name : ", request.params[name]

    number, results = None, {}
    errors = None
    searched = None
    if request.POST and form.validate():
        # we only keep keys with non-empty values
        data = dict([(id,field.value)
                     for (id,field) in form.render_fields.items()
                     if field.value])
        try:
            # make a query using this data dict
            number, results = catalog.search(**data)
            searched = True
        except Exception, r:
            errors = r
            number, results = 0, {}
        results = [context[i] for i in results]
    return {'request':request,
            # transmit the search data by GET to the add form
            'add_data': urllib.urlencode(request.POST),
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form,
            'number': number,
            'searched':searched,
            'errors': errors,
            'results': results}


def view(context, request):
    return {'request':request,
            'master': get_template(join('templates', 'master.pt')),
            'patient_master': get_template(join('templates', 'patient_master.pt')),
            'logged_in': authenticated_userid(request),
            'items': context.values(),
            'patient':context,
            'patient_url': model_url(context, request)}



def edit(context, request):
    form = FieldSet(models.IPatient)
    form = form.bind(context, data=request.POST or None)
    form.id.set(readonly=True)
    if request.POST and form.validate():
        # don't use the id from the form
        request.POST.pop('Patient--id', None)
        form.sync()
        catalog = virtual_root(context, request).catalogs['patients']
        catalog.reindex_doc(int(context.id), context)
        return HTTPFound(location=model_url(context, request))
    return {'patient': context,
            'patient_url': model_url(context, request),
            'request': request,
            'master': get_template('templates/master.pt'),
            'patient_master': get_template(join('templates', 'patient_master.pt')),
            'logged_in': authenticated_userid(request),
            'form': form}


