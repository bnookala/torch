import config
import json
import requests
from flask import Flask, request, abort
app = Flask(__name__)

def _get_host_or_404(screen):
    host = config.wick_daemons.get(screen, None)

    if not host:
        abort(404)

    return host

def _stringify_request_uri(host, screen, cmd):
    return 'http://' + host + '/' + screen + '/' + cmd

def _stringify_simple_uri(host, cmd):
    return 'http://' + host + '/' + cmd

def control_access(fn):
    def wrapped(screen):
        user = request.headers.get('X-User')
        passed_channel = request.headers.get('X-Channel')
        if passed_channel not in config.screen_to_channels(screen):
            return json.dumps({'success': False, 'msg': "you can't do that from this channel, %s" % user})
        return fn(screen)
    return wrapped

@app.route('/list', methods=['GET'])
def list_screens():
    channel = request.headers.get('X-Channel', None)
    if channel:
        return json.dumps(config.channel_to_screens[channel])

@app.route('/enumerate', methods=['GET'])
def enumerate_screens():
    channel = request.headers.get('X-Channel', None)
    if channel:
        for screen in config.channel_to_screens[channel]:
            requests.post(_stringify_simple_uri(_get_host_or_404(screen), screen, 'enumerate'))
        return "enumerating..."

@app.route('/<screen>/list', methods=['GET'])
@control_access
def list_tabs(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.get(_stringify_request_uri(host, screen, 'tabs'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/details', methods=['GET'])
@control_access
def tab_details(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.get(_stringify_request_uri(host, screen, 'active_tab'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/show', methods=['GET'])
@control_access
def show(screen):
    pass

@app.route('/<screen>/close', methods=['GET'])
def close(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'close_tab'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/refresh', methods=['GET'])
@control_access
def refresh(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'reload'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/next', methods=['GET'])
def next(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'next_tab'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/prev', methods=['GET'])
def previous(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'prev_tab'))
    return json.dumps(wick_req.json)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
