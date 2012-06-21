from pyramid.response import Response
from pyramid.view import view_config

@view_config()
def send_command(context, request):
    return Response(context, content_type='text/plain')
