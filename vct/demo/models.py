import transaction
import couchdbkit
from formalchemy.ext import couchdb
from webob import Response

server = None

class Patient(couchdbkit.schema.Document):
    lastName = couchdbkit.StringProperty(required=True)
    firstname = couchdbkit.StringProperty(required=True)
    birthday = couchdbkit.DateProperty()
    sex = couchdbkit.StringProperty()


def initialize_couchdb(db_string):
    global server
    server = couchdbkit.Server()
    db = server.get_or_create_db('patients')


