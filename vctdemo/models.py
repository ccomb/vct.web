from persistent.list import PersistentList
from persistent import Persistent
from repoze.bfg.security import Allow
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from zope.interface import Interface, implements
from zope.schema import TextLine, Int, Text, Datetime, Bytes, Password, List, Choice

class VctRoot(Folder):
    __parent__ = __name__ = None
    __acl__ = [ (Allow, 'group:admins', 'admin'),
                (Allow, 'group:admins', 'view'),
                (Allow, 'group:admins', 'edit'),
                (Allow, 'group:users',  'view'),
                (Allow, 'group:users',  'edit')
                ]



def appmaker(zodb_root):
    updated = False
    #reordered model root followed by catalog
    if 'app_root' not in zodb_root:
        zodb_root['app_root'] = VctRoot()
        zodb_root['app_root'].catalogs = Folder()
        import transaction; transaction.commit()
    if 'users' not in zodb_root['app_root']:
        zodb_root['app_root']['users'] = UserContainer()
        zodb_root['app_root']['users'].__parent__ = zodb_root['app_root']
        zodb_root['app_root']['users'].__name__ = 'users'
        import transaction; transaction.commit()
    if 'users' not in zodb_root['app_root'].catalogs:
        zodb_root['app_root'].catalogs['users'] = Catalog()
        zodb_root['app_root'].catalogs['users']['username'] = CatalogTextIndex('username')
        import transaction; transaction.commit()
    if 'patients' not in zodb_root['app_root']:
        zodb_root['app_root']['patients'] = PatientContainer()
        zodb_root['app_root']['patients'].__parent__ = zodb_root['app_root']
        zodb_root['app_root']['patients'].__name__ = 'patients'
        import transaction; transaction.commit()
    if 'patients' not in zodb_root['app_root'].catalogs:
        zodb_root['app_root'].catalogs['patients'] = Catalog()
        zodb_root['app_root'].catalogs['patients']['id'] = CatalogFieldIndex('id')
        zodb_root['app_root'].catalogs['patients']['firstname'] = CatalogTextIndex('firstname')
        zodb_root['app_root'].catalogs['patients']['name'] = CatalogTextIndex('name')
        zodb_root['app_root'].catalogs['patients']['birthdate'] = CatalogTextIndex('birthdate')
        zodb_root['app_root'].catalogs['patients']['sex'] = CatalogTextIndex('sex')
        import transaction; transaction.commit()
    return zodb_root['app_root']


class UserContainer(Folder):
    pass

from vctdemo.security import GROUPS

class IUser(Interface):
    username = TextLine(title=u'User name')
    password = Password(title=u'password')
    groups = List(title=u'groups', value_type=Choice(title=u'group', values=GROUPS))


class User(Persistent):
    implements(IUser)
    username = password = groups = None

    def __init__(self):
        self.group = PersistentList()


# TODO : rename Patient to Record
class PatientContainer(Folder):
    pass


class IPatient(Interface):
    id = TextLine(title=u'Identification nr')
    name = TextLine(title=u'Name')
    firstname = TextLine(title=u'First Name')
    birthdate = TextLine(title=u'Birthdate')
    # sex = Choice(title=u'Sex', values=['Male', 'Female', 'Unknown'])
    sex = TextLine(title=u'Sex')


class Patient(Folder):
    implements(IPatient)
    id = name = firstname = birthdate = sex = None


class IItem(Interface):
    """an item
        Considered to be placed at the top, as a root for all other classes ??????
    """
    id = TextLine(title=u'Id', description=u'Identifier of the item')
    author = TextLine(title=u'Author', description=u'The author of the item')
    #version = Int(title=u'Version', description=u'The version of the item')


class IPatientItem(Interface):
    date = Datetime(title=u'Date, time', description=u'Date and time')
    title = TextLine(title=u'Title', description=u'The title of the item')
    text = Text(title=u'content', description=u'observation content', required=False)

class PatientItem(Folder):
    id = date = None
    title = text = ''
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
    status = TextLine(title=u"status", description=u"status of the action", required=False)
    image = Bytes(title=u"attached file", description=u"attached file", required=False)
    link = TextLine(title=u"Link",
                    description=u'<a href="https://telemed.ipath.ch/ipath/object/view/292741&amp;user=saliez">case nr 292741</a>',
                    required=False)


class Action(PatientItem):
    implements(IAction)
    status = image = link = ''


class IRelation(PatientItem):
    """the relation between medical items
    """


class Relation(object):
    pass







