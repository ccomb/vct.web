import transaction

from webob import Response

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Unicode

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

metadata = MetaData()

class Model(object):
    def __init__(self, name=''):
        self.name = name

models_table = Table(
    'models',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(255), unique=True),
    )

models_mapper = mapper(Model, models_table)

def populate():
    session = DBSession()
    model = Model(name=u'root')
    session.add(model)
    session.flush()
    transaction.commit()

def initialize_sql(db_string, echo=False):
    engine = create_engine(db_string, echo=echo)
    DBSession.configure(bind=engine)
    metadata.bind = engine
    metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        pass

class HELLO:
    def __init__(self, context, request):
        self.context = context
        self.request = request
    def __call__(self):
        return Response("class HELLO def __call__(self)")

class Item:
    itemID = 1
    version = 1
    time = None
    author = "saliez"
    certainty = 0.5
    type = "generic-type"
    def __init__(self, context, request):
        self.context = context
        self.request = request
#    def __call__(self):
#        return Response("Item Response") 

class Agent(Item):
    type = None

class CareProvider(Agent):
    careProviderID = None

class CareTeam(CareProvider):
    careTeamID = None
    careteamname = "PatientCareTeam"

class Patient(Agent):
    patientID = "123456"
    lastName = "DUPONT"
    firstname = "Jean"
    partner = None
    birthday = None
    sex = None

class MedData(Item):
    medDataID = None
    patient = None
    type = None

class Observation(MedData):
    type = None
    linkProblems = None
    linkActions = None

class Problem(MedData):
    type = None
    linkObservations = None
    linkActions = None

class Action(MedData):
    type = None
    linkProblems = None
    linkObservations = None
    status = None

class Overview(Item):
    overviewName = None
