from vct.demo.models import DBSession
from vct.demo.models import Model

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(Model).filter(Model.name==u'root').first()
    return {'root':root, 'project':'vct.demo'}


def vue_patient(request):
    noms = [request.urlvars['nom']] * 2
    return {'patients': noms}



