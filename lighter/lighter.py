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

def control_access(fn):
    def wrapped(screen):
        user = request.headers.get('X-User')
        passed_channel = request.headers.get('X-Channel')
        needed_channel = config.screen_to_channel(screen)
        if passed_channel != needed_channel:
            return json.dumps({'success': False, 'msg': "you can't do that from this channel, %s" % user})
        return fn(screen)
    return wrapped

@app.route('/list', methods=['GET'])
def list():
    pass

@app.route('/enumerate', methods=['GET'])
def enumerate():
    pass

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
@control_access
def close(screen):
    pass

@app.route('/<screen>/refresh', methods=['GET'])
@control_access
def refresh(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'reload'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/next', methods=['GET'])
@control_access
def next(screen):
    host = _get_host_or_404(screen)
    pass

@app.route('/<screen>/previous', methods=['GET'])
@control_access
def previous(screen):
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0')
