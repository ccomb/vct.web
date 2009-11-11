from couchdbkit.loaders import FileSystemDocsLoader
from formalchemy.ext import couchdb
from webob import Response
import couchdbkit
import os
import transaction
import vct.demo

server = None
db = None

class Patient(couchdbkit.schema.Document):
    firstname = couchdbkit.schema.StringProperty(required=True)
    lastname = couchdbkit.schema.StringProperty(required=True)
    birthday = couchdbkit.schema.DateProperty()
    sex = couchdbkit.schema.StringProperty()


def initialize_couchdb(db_string):
    server = couchdbkit.Server()
    db = server.get_or_create_db('patients')
    couchdbkit.contain(db, Patient)
    vctdir = os.path.dirname(vct.demo.__file__)
    loader = FileSystemDocsLoader(os.path.join(vctdir, '_design'))
    loader.sync(db, verbose=True)


