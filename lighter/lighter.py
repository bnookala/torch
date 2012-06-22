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
        import ipdb; ipdb.set_trace()
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
def show(screen):
    index = request.args['tab']
    if not index:
        # We need the tab index to continue
        abort(404)

    host = _get_host_or_404(screen)

    try:
        # index is a tab value
        index = int(index)
    except ValueError:
        # index is a url
        index = str(index)

    if type(index) is int:
        # Tab index means we can just activate the specific tab instance
        payload = "index=" + str(index)
        wick_req = requests.post(
                        _stringify_request_uri(host, screen, 'activate_tab'),
                        data=payload
                    )
        return "ok"
    else:
        # Otherwise if it is a string, then attempt to search http://y/ for it
        wick_req = requests.get(_stringify_request_uri(host, screen, 'tabs'))
        open_tabs = wick_req.json

        y_req = requests.get('http://y/' + index)

        # A 200 response means http://y/ has a short link
        if y_req.status_code == 200:
            new_url = y_req.url
            for k, v in open_tabs.iteritems():
                if v['url'] == new_url:
                    payload = "index=" + str(k)
                    wick_req = requests.post(
                                    _stringify_request_uri(host, screen, 'activate_tab'),
                                    data=payload
                                )
                    break
                return "ok"
        else:
            # Else interpret as an actual URL and attempt to load the tab
            payload = "url=" + str(index)
            wick_req = requests.post(
                        _stringify_request_uri(host, screen, 'new_tab'),
                        data=payload
                    )
            return "ok"

@app.route('/<screen>/close', methods=['GET'])
@control_access
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
@control_access
def next(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'next_tab'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/prev', methods=['GET'])
@control_access
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
    app.debug=True
    app.run(host='0.0.0.0')
