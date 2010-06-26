from formalchemy.ext.zope import FieldSet
from os.path import join
from repoze.bfg.chameleon_zpt import get_template, render_template_to_response
from repoze.bfg.security import authenticated_userid
from repoze.bfg.traversal import virtual_root
from repoze.bfg.url import model_url
from repoze.bfg.view import static, render_view
from vctdemo import models
from webob import Response
from webob.exc import HTTPFound
import datetime

def listview(context, request):
    """item list (in the context of patient)
    """
    items = context.values()
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
    else:
        pitem = models.PatientItem()
        item_interface = models.IPatientItem
        template = 'patient_item_add.pt'
    pitem.date = datetime.datetime.now()
    form = FieldSet(item_interface)
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
    return render_template_to_response(join('templates', template),
            request=request,
            context=context,
            patient=context,
            patient_url=model_url(context, request),
            patient_master=get_template(join('templates', 'patient_master.pt')),
            master=get_template(join('templates', 'master.pt')),
            logged_in=authenticated_userid(request),
            form=form)


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
            'patient_url':model_url(context, request),
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
            'patient_url':model_url(context.__parent__, request),
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
            'patient_url':model_url(context.__parent__, request),
            'patient_master': get_template('templates/patient_master.pt'),
            'logged_in': authenticated_userid(request),
            'form': form}


def image(context, request):
    response = Response(context.image)
    # XXX
    response.headers['Content-Type'] = 'image/jpg'
    return response


