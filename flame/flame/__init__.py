from pyramid.config import Configurator

from flame.models import Screen, Command
from flame.views import send_command

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    def get_root(self):
        return(Screen())
    config = Configurator(root_factory=get_root, settings=settings)
    config.scan()
    return config.make_wsgi_app()
