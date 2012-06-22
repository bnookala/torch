from pyramid.response import Response
import requests

from pyramid.view import view_config

import config
from models import Command

def channel_permissions(context, request):
    return config.CHANNEL[context.screen] == request.params.get('channel')

def send_command(command, screen):
    result = requests.get(config.SCREEN_TO_ADDRESS[screen])


@view_config(context=Command, renderer='jsonp')
def handle_command(context, request):
    print request
    if not channel_permissions(context, request):
        return {
            'success': False,
            'msg': 'Permission Denied',
        }
    success = command.execute()
    if success:
        return {
            'success': True,
            'command': context.command,
            'screen': context.screen,
            'address': config.SCREEN_TO_ADDRESS[context.screen],
        }
    return {
        'success': False,
        'msg': 'error sending command to wick',
        'command': context.command,
        'screen': context.screen,
        'address': config.SCREEN_TO_ADDRESS[context.screen],
    }
