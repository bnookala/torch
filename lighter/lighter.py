import config
import json
import re
import requests
from flask import Flask, request, abort
app = Flask(__name__)

def _get_host_or_404(screen):
    host = config.wick_daemons.get(_screen_to_prefix(screen).group(1), None)

    if not host:
        abort(404)

    return host

def _stringify_request_uri(host, screen, cmd):
    return 'http://' + host + '/' + screen + '/' + cmd

def _stringify_simple_uri(host, cmd):
    return 'http://' + host + '/' + cmd

def _screen_to_prefix(screen):
	return re.match(r'(.*[^0-9])[0-9]+', screen)

def control_access(fn):
    def wrapped(screen):
        user = request.headers.get('X-User')
        passed_channel = request.headers.get('X-Channel')
        if passed_channel not in config.prefix_to_channels.get(_screen_to_prefix(screen).group(1), {}):
            return json.dumps({'success': False, 'msg': "you can't do that from this channel, %s" % (user or 'jerk')})
        return fn(screen)
    return wrapped

@app.route('/list', methods=['GET'])
def list_screens():
    channel = request.headers.get('X-Channel', None)
    if channel:
        return json.dumps(config.channel_to_prefixes[channel])

@app.route('/enumerate', methods=['GET'])
def enumerate_screens():
    channel = request.headers.get('X-Channel', None)
    if channel:
        for screen in config.channel_to_prefixes[channel]:
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

@app.route('/register_prefix', methods=['POST'])
def register_prefix():
	config.wick_daemons[request.form['prefix']] = request.remote_addr + ':' + request.form['port']
	print "wick daemons:"
	print config.wick_daemons
	return 'ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
