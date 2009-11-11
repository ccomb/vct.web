from repoze.bfg.router import make_app

import vct.demo
from vct.demo.models import initialize_couchdb

class Cleanup:
    def __init__(self, cleaner):
        self.cleaner = cleaner
    def __del__(self):
        self.cleaner()

def handle_teardown(event):
    environ = event.request.environ

def app(global_config, **kw):
    """ This function returns a repoze.bfg.router.Router object.

    It is usually called by the PasteDeploy framework during ``paster serve``.
    """
    db_string = kw.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    initialize_couchdb(db_string)
    return make_app(None, vct.demo, options=kw)

