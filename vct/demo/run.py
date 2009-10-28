from repoze.bfg.router import make_app

import vctdemo
from vctdemo.models import DBSession
from vctdemo.models import initialize_sql

class Cleanup:
    def __init__(self, cleaner):
        self.cleaner = cleaner
    def __del__(self):
        self.cleaner()

def handle_teardown(event):
    environ = event.request.environ
    environ['vctdemo.sasession'] = Cleanup(DBSession.remove)

def app(global_config, **kw):
    """ This function returns a repoze.bfg.router.Router object.
    
    It is usually called by the PasteDeploy framework during ``paster serve``.
    """
    db_string = kw.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    initialize_sql(db_string)
    return make_app(None, vctdemo, options=kw)

