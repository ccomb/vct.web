from vctdemo.models import DBSession
from vctdemo.models import Model

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(Model).filter(Model.name==u'root').first()
    return {'root':root, 'project':'vct.demo'}
