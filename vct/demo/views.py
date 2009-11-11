from formalchemy.ext import couchdb
from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.view import static
from webob import Response
from webob.exc import HTTPFound
from models import Patient
static_view = static('templates/static')


def home_view(context, request):
    return {'request':request, 'context':context}


def patient_add(context, request):
    p = Patient()
    form = couchdb.FieldSet(p).bind(p, data=request.POST or None)
    if request.POST and form.validate():
        form.sync()
        p.save()
        return HTTPFound(location="/patients/list")

    return {'request':request,
            'context':context,
            'form':form}


class PatientList(object):
    FieldSet = couchdb.FieldSet
    Grid = couchdb.Grid
    model = [Patient]

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        grid = self.Grid(Patient)
        return {'request':self.request,
                'context':self.context,
                'grid':grid}


def patient_edit(context, request):
    return Response(u'patient edit')


def patient_view(context, request):
    return render_template_to_response("templates/patient.pt",
        request = request,
        project = 'vct.demo')

    #return("templates/static/Help/Notifications-Help.html")

