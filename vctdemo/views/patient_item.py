from datetime import datetime, date, timedelta
from formalchemy import Field as FaField
from formalchemy import FieldSet as FaFieldSet
from formalchemy import types
from formalchemy.ext.zope import FieldSet, Field
from os.path import join
from repoze.bfg.chameleon_zpt import get_template, render_template_to_response
from repoze.bfg.security import authenticated_userid
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.bfg.view import static, render_view
from repoze.catalog.indexes.field import CatalogFieldIndex
from vctdemo import models
from webob import Response
from webob.exc import HTTPFound
from zope.interface import providedBy

def _update_catalog(catalog):
    """update the catalog with newer indexes to avoid deleting the db
    """
    if 'item_type' not in catalog:
        catalog['item_type'] = CatalogFieldIndex('item_type')
    if 'date' not in catalog:
        catalog['date'] = CatalogFieldIndex('date')


def listview(context, request):
    """item list (in the context of patient)
    """
    item_type = request.GET.get('type')
    catalog = context.catalogs['items']
    number, results = catalog.search(item_type=item_type)
    items = [context[i] for i in results]

    return {'request':request,
            'context':context,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context,
            'patient_url': model_url(context, request),
            'render_view': render_view,
            'patient_master': get_template(join('templates', 'patient_master.pt')),
            'items':items}


def add(context, request):
    """add item view (in the context of patient)
    """
    item_type = request.GET.get('type')
    if item_type is not None and item_type=='Action':
        pitem = models.Action()
        item_interface = models.IAction
        template = 'patient_action_add.pt'
    elif item_type is not None and item_type=='Issue':
        pitem = models.Issue()
        item_interface = models.IIssue
        template = 'patient_issue_add.pt'
    elif item_type is not None and item_type=='Observation':
        pitem = models.Observation()
        item_interface = models.IObservation
        template = 'patient_observation_add.pt'
    else:
        pitem = models.PatientItem()
        item_interface = models.IPatientItem
        template = 'patient_item_add.pt'
    pitem.date = datetime.now()
    form = FieldSet(item_interface)
    form = form.bind(pitem, data=request.POST or None)
    if request.POST and form.validate():   # if new and valid data
        request.POST.pop('PatientItem--id', None)
        form.sync()
        id = len(context)
        while id in context:
            id += 1
        pitem.id = str(id)
        pitem.author = authenticated_userid(request)
        context[str(id)] = pitem
        catalog = context.catalogs['items']
        # zope.index BUG #598776
        if pitem.text is None:
            pitem.text = u''
        _update_catalog(catalog)
        catalog.index_doc(id, pitem)
        return HTTPFound(location=model_url(pitem, request))
    return render_template_to_response(join('templates', template),  # render the page
            request=request,
            context=context,
            patient=context,
            patient_url=model_url(context, request),
            patient_master=get_template(join('templates', 'patient_master.pt')),
            master=get_template(join('templates', 'master.pt')),
            logged_in=authenticated_userid(request),
            form=form)


class SearchFields(object):
    """class for the search form
    """
    title = FaField()
    text = FaField()
    start = FaField(type=types.Date)
    end = FaField(type=types.Date)
    item_type = FaField().checkbox(
        options=[('item', 'IPatientItem'),
                 ('action', 'IAction'),
                 ('issue', 'IIssue'),
                 ('observation', 'IObservation')])


def search(context, request):
    form = FaFieldSet(SearchFields)
    form.configure(include=[SearchFields.title,
                  SearchFields.text,
                  SearchFields.start,
                  SearchFields.end,
                  SearchFields.item_type])
    form = form.bind(SearchFields, data=request.POST or None)
    catalog = context.catalogs['items']
    number, results = None, {}
    errors = None
    if request.POST and form.validate():
        query = dict([(id,field.value)
                     for (id,field) in form.render_fields.items()
                     if field.value is not None
                     ])
        # replace the 'start' and 'end' dates with a (start, end) tuple
        query['date'] = (datetime.fromordinal(query.pop('start', datetime.min).toordinal()),
                        timedelta(1) + datetime.fromordinal(query.pop('end', datetime.max-timedelta(1)).toordinal()))
        if not query.get('item_type'):
            query['item_type'] = [i[1] for i in SearchFields.item_type.render_opts['options']]
        try:
            number, results = catalog.search(**query)
        except Exception, r:
            errors = r
            number, results = 0, {}
        results = [context[i] for i in results.keys()] if results else ()
    return {'request':request,
            'context':context,
            'patient_url':model_url(context, request),
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context,
            'patient_master': get_template('templates/patient_master.pt'),
            'form': form,
            'number': number,
            'render_view': render_view,
            'errors': errors,
            'results': results}


def view(context, request):
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context.__parent__,
            'patient_url':model_url(context.__parent__, request),
            'patient_master': get_template('templates/patient_master.pt'),
            'context':context}

def edit(context, request):
    iface = list(providedBy(context))[0]
    form = FieldSet(iface)
    form = form.bind(context, data=request.POST or None)
    if request.POST and form.validate():
        request.POST.pop('PatientItem--id', None)
        form.sync()
        catalog = context.__parent__.catalogs['items']
        # zope.index BUG #598776
        if context.text is None:
            context.text = u''
        context.version += 1
        # update the catalog
        _update_catalog(catalog)
        catalog.reindex_doc(int(context.id), context)
        # How to return directly to the list ???
        return HTTPFound(location=model_url(context, request))
    return {'context': context,
            'request': request,
            'master': get_template('templates/master.pt'),
            'patient':context.__parent__,
            'patient_url':model_url(context.__parent__, request),
            'patient_master': get_template('templates/patient_master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}


def image(context, request):
    response = Response(context.image)
    # XXX
    response.headers['Content-Type'] = 'image/jpg'
    return response


def proto_care_plan(context, request):
    return {'request':request,
            'master': get_template('templates/master.pt'),
            'logged_in': authenticated_userid(request),
            'patient':context.__parent__,
            'patient_url': model_url(context, request),
            'patient_master': get_template('templates/patient_master.pt'),
            'context':context}


