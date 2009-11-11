from vct.demo.models import DBSession
from vct.demo.models import Model

from webob import Response

from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.view import static
static_view = static('templates/static')

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(Model).filter(Model.name==u'root').first()
    return {'root':root, 'project':'vct.demo'}


def vue_patient(request):
    noms = [request.urlvars['nom']] * 2
    return {'patients': noms}

def hello(context, request):   # not working ???
    return Response("hello")

def HELLO(context, request):   # sometimes working why well or not ?????????
    return render_template_to_response("templates/HELLO.pt",
        request = request,
        project = 'vct.demo')

def item(context, request):   # not working ???
    return render_template_to_response("templates/item.pt",
        request = request,
        project = 'vct.demo')

def patient_view(context, request):
    return render_template_to_response("templates/patient.pt",
        request = request,
        project = 'vct.demo')

    #return("templates/static/Help/Notifications-Help.html")
   
