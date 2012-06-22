import config
import json
import re
import requests
from flask import Flask, request, abort
app = Flask(__name__)

@app.route('/register_prefix', methods=['POST'])
def register_prefix():
    "Wick instances make requests to this to register the screens they control"
    config.wick_daemons[request.form['prefix']] = request.remote_addr + ':' + request.form['port']
    print "wick daemons:"
    print config.wick_daemons
    return 'ok'

def _get_host_or_404(screen):
    host = config.wick_daemons.get(_screen_to_prefix(screen), None)

    if not host:
        abort(404)

    return host

def _stringify_request_uri(host, screen, cmd):
    return 'http://' + host + '/' + screen + '/' + cmd

def _stringify_simple_uri(host, cmd):
    return 'http://' + host + '/' + cmd

def _screen_to_prefix(screen):
    return re.match(r'(.*[^0-9])[0-9]+', screen).group(1)

def control_access(fn):
    def wrapped(screen):
        user = request.headers.get('X-User')
        channel = request.headers.get('X-Channel')
        if channel not in config.prefix_to_channels.get(_screen_to_prefix(screen), {}):
            return "you can't fuck with %s from %s, %s" % (screen, channel, (user or 'jerk'))
        return fn(screen)
    return wrapped

@app.route('/list', methods=['GET'])
def list_screens():
    screens = []
    channel = request.headers.get('X-Channel', None)
    prefixes = config.channel_to_prefixes.get(channel, [])
    for prefix in prefixes:
        host = config.wick_daemons.get(prefix)
        if host:
            screens_on_wick = requests.get(_stringify_simple_uri(host, 'list')).json
            screens.extend(screens_on_wick)
    screens = sorted(set(screens))
    return ', '.join(sorted(screens)) if screens else 'sorry, no screens for you'

@app.route('/enumerate', methods=['GET'])
def enumerate_screens():
    channel = request.headers.get('X-Channel', None)
    if channel:
        for prefix in config.channel_to_prefixes[channel]:
            if prefix in config.wick_daemons:
                requests.post(_stringify_simple_uri(config.wick_daemons[prefix], 'enumerate'))
    return "enumerating..."

@app.route('/<screen>/list', methods=['GET'])
def list_tabs(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.get(_stringify_request_uri(host, screen, 'tabs'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/details', methods=['GET'])
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

        y_req = requests.get('http://y/' + index, timeout=5)

        if y_req.status_code == 200:
            # A 200 response means http://y/ has a short link
            new_url = y_req.url
        else:
            # Else interpret as an actual URL
            new_url = str(index)

        # Try to find the url among the open tabs and activate it if found
        for k, v in open_tabs.iteritems():
            if v['url'] == new_url:
                wick_req = requests.post(
                                _stringify_request_uri(host, screen, 'activate_tab'),
                                data={'index': k}
                            )
                return "ok, i showed that for you" if wick_req.status_code == 200 else "something went wrong showing you that tab"
        # If not found, open in a new tab
        wick_req = requests.post(
                    _stringify_request_uri(host, screen, 'new_tab'),
                    data={'url': new_url},
                )
        return "ok" if wick_req.status_code == 200 else "something went wrong opening that for you. it may be an omen."

@app.route('/<screen>/close', methods=['GET'])
def close(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.post(_stringify_request_uri(host, screen, 'close_tab'))
    return json.dumps(wick_req.json)

@app.route('/<screen>/refresh', methods=['GET'])
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

@app.route('/<screen>/fullscreen_on', methods=['GET'])
def fullscreen_on(screen):
    host = _get_host_or_404(screen)
    wick_req = requests.post(_stringify_request_uri(host, screen, 'fullscreen_on'))
    return wick_req.text

@app.route('/<screen>/fullscreen_off', methods=['GET'])
def fullscreen_off(screen):
    host = _get_host_or_404(screen)
    wick_req = requests.post(_stringify_request_uri(host, screen, 'fullscreen_off'))
    return wick_req.text

@app.route('/<screen>/rotate', methods=['GET'])
def rotate(screen):
    host = _get_host_or_404(screen)
    rotate = request.args['enabled']
    if not rotate:
        abort(404)
    return 'ok'

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
