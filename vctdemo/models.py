# coding: utf-8
from persistent import Persistent
from persistent.list import PersistentList
from repoze.bfg.security import Allow
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.folder import Folder
from zope.annotation import factory
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import adapts
from zope.interface import Interface, implements, Attribute, providedBy
from zope.schema import TextLine, Text, Datetime, Bytes, Password, List, Choice

class VctRoot(Folder):
    __parent__ = __name__ = None
    __acl__ = [ (Allow, 'group:admins', 'admin'),
                (Allow, 'group:admins', 'view'),
                (Allow, 'group:admins', 'edit'),
                (Allow, 'group:users',  'view'),
                (Allow, 'group:users',  'edit')
                ]



def appmaker(zodb_root):
    #reordered model root followed by catalog
    if 'app_root' not in zodb_root:
        zodb_root['app_root'] = VctRoot()
        zodb_root['app_root'].catalogs = Folder()
        import transaction; transaction.commit()
    # user root definition
    if 'users' not in zodb_root['app_root']:
        zodb_root['app_root']['users'] = UserContainer()
        zodb_root['app_root']['users'].__parent__ = zodb_root['app_root']
        zodb_root['app_root']['users'].__name__ = 'users'
        import transaction; transaction.commit()
    # user catalog definition
    if 'users' not in zodb_root['app_root'].catalogs:
        zodb_root['app_root'].catalogs['users'] = Catalog()
        zodb_root['app_root'].catalogs['users']['username'] = CatalogTextIndex('username')
        import transaction; transaction.commit()
    #patient definition and catalogs
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


class UserContainer(Folder):  # The folder containing the users
    pass

from vctdemo.security import GROUPS

class IUser(Interface):
    username = TextLine(title=u'User name')
    password = Password(title=u'password')
    groups = List(title=u'groups', value_type=Choice(title=u'group', values=GROUPS))  # ??? Make a list of checkboxes
    organization = TextLine(title=u'Organization', required=False)
    address = TextLine(title=u'Address', required=False)
    city = TextLine(title=u'City', required=False)
    phone = TextLine(title=u'phone', required=False)


class User(Persistent):
    # IAttributeAnnotatable because our user must be able to store annotations
    implements(IUser, IAttributeAnnotatable)
    username = password = groups = organization = language = None
    address = city = phone = initial_patient_view = None
    def __init__(self):
        # storing a list in the zodb requires PersistentList
        self.group = PersistentList()
        self.language = 'english'
        #initial_patient_view = "default Start View"


class IUserPreferences(Interface):
    language = Choice(title=u'preferred language', values=[
        u'english', u'french', u'spanish', u'german', u'greek', u'turkish'], required=False)
    initial_patient_view = TextLine(title=u'Initial Patient View', required=False)


class UserPreferences(Persistent):
    """adapter for user preferences
    """
    implements(IUserPreferences)
    adapts(IUser)
    #def __init__(self):
    #    self.language = 'english'

# the annotation factory allows to create the annotation adatper
user_preferences = factory(UserPreferences)


# TODO : rename Patient to Record
class PatientContainer(Folder):
    pass


class IPatient(Interface):
    id = TextLine(title=u'Identification nr')
    name = TextLine(title=u'Last Name')
    firstname = TextLine(title=u'First Name')
    birthdate = TextLine(title=u'Birthdate')
    # choice is not working ???
    # sex = Choice(title=u'Sex', values=['Male', 'Female', 'Unknown'])
    sex = TextLine(title=u'Sex')
    address = TextLine(title=u'Address', required=False)
    postal_code = TextLine(title=u'Postal Code', required=False)
    city = TextLine(title=u'City', required=False)
    insurances = TextLine(title=u'Insurance(s)', required=False)

class Patient(Folder):
    implements(IPatient, IAttributeAnnotatable)
    #implements(IPatientAdmin)
    id = name = firstname = birthdate = sex = None
    address = postal_code = city = insurances = None


class IItem(Interface):
    """an item
        Considered to be placed at the top, as a root for all other classes ??????
    """
    id = TextLine(title=u'Id', description=u'Identifier of the item')
    author = TextLine(title=u'Author', description=u'The author of the item')
    #version = Int(title=u'Version', description=u'The version of the item')
    item_type = Attribute(u"Item type")


class IPatientItem(Interface):
    date = Datetime(title=u'Date, time', description=u'Date and time')
    title = TextLine(title=u'Title', description=u'The title of the item')
    text = Text(title=u'content', description=u'observation content', required=False)
    status = TextLine(title=u"status", description=u"status of the action", required=False)
    image = Bytes(title=u"attached file", description=u"attached file", required=False)
    link = TextLine(title=u"Link", description=u'(Link to an external annex)', required=False)

class PatientItem(Folder):
    id = date = None
    title = text = ''
    status = image = link = ''
    implements(IPatientItem)

    @property
    def item_type(self):
        return list(providedBy(self).interfaces())[0].__name__


class IObservation(IPatientItem):
    pass


class Observation(PatientItem):
    implements(IObservation)


class IIssue(IPatientItem):
    pass


class Issue(PatientItem):
    implements(IIssue)


class IAction(IPatientItem):
    pass

class Action(PatientItem):
    implements(IAction)


class IRelation(IPatientItem):
    """the relation between medical items
    """
    source = Attribute(u"source")
    destination = Attribute(u"destination")

class Relation(PatientItem):
    """relation between two items
    """
    implements(IRelation)


class IRelations(Interface):
    """interface of the relation container
    """
    relations = Attribute(u"relations")


class Relations(Persistent):
    """ the relation container
    """
    implements(IRelations)
    adapts(IPatient)
    relations = None

    def __init__(self):
        if self.relations is None:
            self.relations = PersistentList()


relations = factory(Relations)






