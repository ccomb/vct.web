from persistent import Persistent
from repoze.bfg.security import Allow
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from zope.interface import Interface, implements
from zope.schema import TextLine, Int, Text, Datetime, Bytes

class VctRoot(Folder):
    __parent__ = __name__ = None
    __acl__ = [ (Allow, 'group:admins', 'view'), (Allow, 'group:admins', 'edit') ]



def appmaker(zodb_root):
    updated = False
    if 'app_root' not in zodb_root:
        zodb_root['app_root'] = VctRoot()
        zodb_root['app_root'].catalogs = Folder()
        import transaction; transaction.commit()
    if 'users' not in zodb_root['app_root'].catalogs:
        zodb_root['app_root'].catalogs['users'] = Catalog()
        zodb_root['app_root'].catalogs['users']['username'] = CatalogTextIndex('username')
        import transaction; transaction.commit()
    if 'patients' not in zodb_root['app_root'].catalogs:
        zodb_root['app_root'].catalogs['patients'] = Catalog()
        zodb_root['app_root'].catalogs['patients']['id'] = CatalogFieldIndex('id')
        zodb_root['app_root'].catalogs['patients']['firstname'] = CatalogTextIndex('firstname')
        zodb_root['app_root'].catalogs['patients']['name'] = CatalogTextIndex('name')
        zodb_root['app_root'].catalogs['patients']['birthdate'] = CatalogTextIndex('birthdate')
        zodb_root['app_root'].catalogs['patients']['sex'] = CatalogTextIndex('sex')
        import transaction; transaction.commit()
    if 'patients' not in zodb_root['app_root']:
        zodb_root['app_root']['patients'] = PatientContainer()
        zodb_root['app_root']['patients'].__parent__ = zodb_root['app_root']
        zodb_root['app_root']['patients'].__name__ = 'patients'
        import transaction; transaction.commit()
    if 'users' not in zodb_root['app_root']:
        zodb_root['app_root']['users'] = UserContainer()
        zodb_root['app_root']['users'].__parent__ = zodb_root['app_root']
        zodb_root['app_root']['users'].__name__ = 'users'
        import transaction; transaction.commit()
    return zodb_root['app_root']


class UserContainer(Folder):
    pass


class IUser(Interface):
    username = TextLine(title=u'User name')


class User(Persistent):
    implements(IUser)
    username = None


# TODO : rename Patient to Record
class PatientContainer(Folder):
    pass


class IPatient(Interface):
    id = TextLine(title=u'Identification nr')
    name = TextLine(title=u'Name')
    firstname = TextLine(title=u'First Name')
    birthdate = TextLine(title=u'Birthdate')
    sex = TextLine(title=u'Sex', required=False)


class Patient(Folder):
    implements(IPatient)
    id = name = firstname = birthdate = sex = None


class IItem(Interface):
    """an item
    """
    id = TextLine(title=u'Id', description=u'Identifier of the item')
    author = TextLine(title=u'Author', description=u'The author of the item')
    #version = Int(title=u'Version', description=u'The version of the item')


class IPatientItem(Interface):
    date = Datetime(title=u'Date, time', description=u'Date and time')
    title = TextLine(title=u'Title', description=u'The title of the item')
    text = Text(title=u'content', description=u'observation content')

class PatientItem(Folder):
    id = date = title = text = None
    implements(IItem, IPatientItem)


class IObservation(IPatientItem):
    pass


class Observation(PatientItem):
    implements(IObservation)


class IIssue(IPatientItem):
    pass


class Issue(PatientItem):
    implements(IIssue)


class IAction(IPatientItem):
    status = TextLine(title=u"status", description=u"status of the action")
    image = Bytes(title=u"attached file", description=u"attached file")


class Action(PatientItem):
    implements(IAction)
    status = image = None


class IRelation(PatientItem):
    """the relation between medical items
    """


class Relation(object):
    pass







