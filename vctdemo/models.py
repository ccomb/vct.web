from persistent import Persistent
from repoze.bfg.security import Allow
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from zope.interface import Interface, implements
from zope.schema import TextLine, Int

class VctRoot(Folder):
    __parent__ = __name__ = None
    __acl__ = [ (Allow, 'group:admins', 'view'), (Allow, 'group:admins', 'edit') ]



def appmaker(zodb_root):
    updated = False
    if 'app_root' not in zodb_root:
        zodb_root['app_root'] = VctRoot()
        zodb_root['app_root'].catalogs = Folder()
        zodb_root['app_root'].catalogs['patients'] = Catalog()
        zodb_root['app_root'].catalogs['patients']['id'] = CatalogFieldIndex('id')
        zodb_root['app_root'].catalogs['patients']['firstname'] = CatalogTextIndex('firstname')
        zodb_root['app_root'].catalogs['patients']['name'] = CatalogTextIndex('name')
        import transaction; transaction.commit()
    if 'patients' not in zodb_root['app_root']:
        zodb_root['app_root']['patients'] = PatientContainer()
        zodb_root['app_root']['patients'].__parent__ = zodb_root['app_root']
        zodb_root['app_root']['patients'].__name__ = 'patients'
        import transaction; transaction.commit()
    return zodb_root['app_root']


class PatientContainer(Folder):
    pass


class IPatient(Interface):
    id = TextLine(title=u'Id', description=u'Identifier of the patient')
    name = TextLine(title=u'Name', description=u'Name of the patient')
    firstname = TextLine(title=u'First Name', description=u'First Name of the patient')

class Patient(Folder):
    implements(IPatient)
    firstname = name = id = None





class MedItem(Persistent):
    author = TextLine(title=u'Author', description=u'The author of the item')
    version = Int(title=u'Version', description=u'The version of the item')


class Observation(MedItem):
    pass


class Issue(MedItem):
    pass


class Action(MedItem):
    pass
