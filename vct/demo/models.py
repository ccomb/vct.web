import transaction
import couchdbkit
from formalchemy.ext import couchdb
from webob import Response

server = None
db = None

class Patient(couchdbkit.schema.Document):
    lastName = couchdbkit.schema.StringProperty(required=True)
    firstname = couchdbkit.schema.StringProperty(required=True)
    birthday = couchdbkit.schema.DateProperty()
    sex = couchdbkit.schema.StringProperty()


def initialize_couchdb(db_string):
    global server
    server = couchdbkit.Server()
    db = server.get_or_create_db('patients')


