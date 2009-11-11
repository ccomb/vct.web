from webob import Response

from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.view import static
static_view = static('templates/static')


def home_view(context, request):
    return {'request':request, 'context':context}


def patient_add(context, request):
    return {'request':request, 'context':context}


def patient_list(context, request):
    return {'request':request, 'context':context}


def patient_edit(context, request):
    return Response(u'patient edit')


def patient_view(context, request):
    return render_template_to_response("templates/patient.pt",
        request = request,
        project = 'vct.demo')

    #return("templates/static/Help/Notifications-Help.html")

