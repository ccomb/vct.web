from pyramid.config import Configurator
from vctweb.resources import Root
from vctweb import views

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)

    config.add_route('home', '/', view=views.home, renderer="templates/home.pt")
    config.add_route('patients_add', '/patients/add', view=views.patient_add, renderer="templates/patient_add.pt")
    config.add_route('patients', '/patients/', view=views.patients, renderer="templates/patients.pt")

    config.add_static_view('static', 'vctweb:static')
    return config.make_wsgi_app()

