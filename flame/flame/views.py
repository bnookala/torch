from pyramid.response import Response
from pyramid.view import view_config

import config
from models import Command

@view_config(context=Command, renderer='jsonp')
def send_command(context, request):
    return {
        'command':context.command,
        'screen':context.screen,
        'address':config.SCREEN_TO_ADDRESS[context.screen],
    }
