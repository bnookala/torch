from pyramid.config import Configurator
from pyramid.renderers import JSONP

from flame.models import Screen, Command
from flame.views import send_command

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    def get_root(self):
        return(Screen())

    config = Configurator(root_factory=get_root, settings=settings)
    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.scan()
    return config.make_wsgi_app()
