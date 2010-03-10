from persistent.mapping import PersistentMapping
from persistent import Persistent
from repoze.folder import Folder
from zope.schema import TextLine, Int

class VctRoot(PersistentMapping):
    __parent__ = __name__ = None

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = VctRoot()
        zodb_root['app_root'] = app_root
        if not 'patients' in app_root:
            app_root['patients'] = PatientContainer()
        import transaction
        transaction.commit()
    return zodb_root['app_root']


class PatientContainer(Folder):
    pass


class Patient(Folder):
    pass


class MedItem(Persistent):
    author = TextLine(title=u'Author', description=u'The author of the item')
    version = Int(title=u'Version', description=u'The version of the item')


class Observation(MedItem):
    pass


class Issue(MedItem):
    pass


class Action(MedItem):
    pass
