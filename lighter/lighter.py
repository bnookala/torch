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
        payload = "index=" + str(index)
        wick_req = requests.post(
                        _stringify_request_uri(host, screen, 'activate_tab'),
                        data=payload
                    )
        return "ok"
    else:
        wick_req = requests.get(_stringify_request_uri(host, screen, 'tabs'))
        open_tabs = wick_req.json

        y_req = requests.get('http://y/' + index)
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
def refresh(screen):
    tab_index = request.form['tab']
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

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
