import config
import json
import os
import cPickle as pickle
import re
import requests
import subprocess
from flask import Flask, request, abort
from urllib2 import urlparse
app = Flask(__name__)

WICK_CACHE = '.wick_daemons'

def safe_request_fn(fn):
    def safe_request(url, *args, **kwargs):
        try:
            return fn(url, *args, **kwargs)
        except requests.ConnectionError:
            # take this host out of the list of wicks
            host = urlparse.urlparse(url).netloc
            bad_wicks = set()
            for key, val in config.wick_daemons.iteritems():
                if host in val:
                    bad_wicks.add(key)
            for wick in bad_wicks:
                del config.wick_daemons[wick]
            pickle.dump(config.wick_daemons, open(WICK_CACHE, 'w'))
            abort(502)
    return safe_request

requests.post = safe_request_fn(requests.post)
requests.get = safe_request_fn(requests.get)

def safe_post(url, *args, **kwargs):
    try:
        requests.post(url, *args, **kwargs)
    except requests.ConnectionError:
        print url + " is very bad"
requests.post = safe_post

@app.route('/register_prefix', methods=['POST'])
def register_prefix():
    "Wick instances make requests to this to register the screens they control"
    config.wick_daemons[request.form['prefix']] = request.remote_addr + ':' + request.form['port']
    pickle.dump(config.wick_daemons, open(WICK_CACHE, 'w'))
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

def _get_y_url(query):
    y_req = requests.get('http://y/' + query, timeout=5)
    if y_req.status_code == 200:
        return y_req.url
    else:
        return None

def control_access(fn):
    def wrapped(screen):
        user = request.headers.get('X-User')
        channel = request.headers.get('X-Channel')
        if channel not in config.prefix_to_channels.get(_screen_to_prefix(screen), {}):
            return "you can't fuck with %s from %s, %s" % (screen, channel, (user or 'jerk'))
        return fn(screen)
    return wrapped

def _list_and_maybe_enumerate(enumerate):
    cmd = 'enumerate' if enumerate else 'list'
    screens = []
    channel = request.headers.get('X-Channel', None)
    prefixes = config.channel_to_prefixes.get(channel, [])
    for prefix in prefixes:
        host = config.wick_daemons.get(prefix)
        if host:
            screens_on_wick = requests.get(_stringify_simple_uri(host, cmd))
            if screens_on_wick and screens_on_wick.json:
                screens.extend(screens_on_wick.json)
    screens = sorted(set(screens))
    return ', '.join(sorted(screens)) if screens else 'sorry, no screens for you'

@app.route('/list', methods=['GET'])
def list_screens():
    return _list_and_maybe_enumerate(enumerate=False)

@app.route('/enumerate', methods=['GET'])
def enumerate_screens():
    return _list_and_maybe_enumerate(enumerate=True)

@app.route('/<screen>/list', methods=['GET'])
def list_tabs(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.get(_stringify_request_uri(host, screen, 'tabs'))
    if not wick_req.json:
        return "%s? i don't know about no %s"

    wick_req_str = ''
    for screen, data in wick_req.json.iteritems():
        wick_req_str += screen + ': ' + data.get('title', '???') + ' (' + data.get('url', '???') + ')\n'
    return wick_req_str

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

        # _get_y_url checks y to see if the alias exists.
        new_url = _get_y_url(index)
        if y_url is None:
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
    time_delay = request.args.get('time', 5)
    if not rotate:
        abort(404)

    f = open('rotate_pids', 'r+')
    pickled_pids = pickle.load(f)
    f.close()
    pid = pickled_pids.get(screen, None)

    if rotate == "true":
        if not pid:
            args = ['./rotate.py', host, screen, str(time_delay)]
            process = subprocess.Popen(args)
            pickled_pids[screen] = process
        else:
            return "Already rotating!"
    else:
        if pid:
            pid.terminate()
            del pickled_pids[screen]
        else:
            return "Not rotating!"

    os.remove('rotate_pids')
    f = open('rotate_pids', 'w+')
    pickle.dump(pickled_pids, f)
    f.close()

    return "ok"

@app.route('/<screen>/peek', methods=['GET'])
def peek(screen):
    host = _get_host_or_404(screen)
    url = request.args['url']
    duration = request.args.get('duration', None)
    if not duration:
        duration = 30
    if duration > 300:
        duration = 300

    args = ['./peek.py', host, screen, url, str(duration)]
    subprocess.Popen(args)
    return "ok, peaking at " + url

@app.route('/nyanwin', methods=['GET'])
def nyanwin():
    if config.nyanwinning:
        return 'be patient'
    config.nyanwinning = True
    # screens should be something like 'consumer1,consumer3,test2'
    config.nyanwin_queue = request.args['screens'].split(',')
    return _next_nyanwin()

@app.route('/nyanwin_done', methods=['GET'])
def nyanwin_done():
    "When one nyanwin is done, queue up the next."
    return _next_nyanwin()

def _next_nyanwin():
    if not config.nyanwin_queue:
        config.nyanwinning = False
        return 'ok'
    screen = config.nyanwin_queue[0]
    config.nyanwin_queue = config.nyanwin_queue[1:]
    host = _get_host_or_404(screen)
    requests.post(_stringify_request_uri(host, screen, 'nyanwin'))
    return 'ok'

if __name__ == "__main__":
    if not os.path.exists('rotate_pids'):
        rotate_pids = {}
        f = open('rotate_pids', 'w')
        pickle.dump(rotate_pids, f)
        f.close()

    try:
        cached_wicks = pickle.load(open(WICK_CACHE, 'r'))
    except IOError:
        cached_wicks = {}
    config.wick_daemons.update(cached_wicks)

    app.debug=True
    app.run(host='0.0.0.0')
