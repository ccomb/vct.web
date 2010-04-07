from formalchemy.ext.zope import FieldSet
from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.security import authenticated_userid
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.bfg.view import static
from vctdemo import models
from webob.exc import HTTPFound
import datetime

def list(context, request):
    items = context.values()
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context,
            'patient_master': get_template('templates/patient_master.pt'),
            'items':items}


def add(context, request):
    pitem = models.PatientItem()
    pitem.date = datetime.datetime.now()
    form = FieldSet(models.IPatientItem)
    form = form.bind(pitem, data=request.POST or None)
    if request.POST and form.validate():
        request.POST.pop('PatientItem--id', None)
        form.sync()
        id = len(context)
        while id in context:
            id += 1
        pitem.id = str(id)
        pitem.author = authenticated_userid(request)
        context[str(id)] = pitem
        catalog = context.catalogs['items']
        catalog.index_doc(id, pitem)
        return HTTPFound(location=model_url(pitem, request))
    return {'request':request,
            'context':context,
            'patient':context,
            'patient_master': get_template('templates/patient_master.pt'),
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}


def search(context, request):
    pitem = models.PatientItem()
    form = FieldSet(models.IPatientItem)
    form.configure(exclude=[form.date])
    for field in form.render_fields:
        getattr(form, field).set(required=False)
    form = form.bind(pitem, data=request.POST or None)
    catalog = context.catalogs['items']
    number, results = None, {}
    errors = None
    if request.POST and form.validate():
        data = dict([(id,field.value)
                     for (id,field) in form.render_fields.items()
                     if field.value])
        try:
            number, results = catalog.search(**data) # XXX
        except Exception, r:
            errors = r
            number, results = 0, {}
        results = [context[i] for i in dict(results).keys()]
    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context,
            'patient_master': get_template('templates/patient_master.pt'),
            'form': form,
            'number': number,
            'errors': errors,
            'results': results}


def view(context, request):
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context.__parent__,
            'patient_master': get_template('templates/patient_master.pt'),
            'context':context}



def edit(context, request):
    form = FieldSet(models.IPatientItem)
    form = form.bind(context, data=request.POST or None)
    if request.POST and form.validate():
        request.POST.pop('PatientItem--id', None)
        form.sync()
        catalog = context.__parent__.catalogs['items']
        catalog.reindex_doc(int(context.id), context)
        return HTTPFound(location=model_url(context, request))
    return {'context': context,
            'request': request,
            'master': get_template('templates/master.pt'),
            'patient':context.__parent__,
            'patient_master': get_template('templates/patient_master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}


