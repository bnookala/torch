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

@app.route('/list', methods=['GET'])
def list():
    pass

@app.route('/enumerate', methods=['GET'])
def enumerate():
    pass

@app.route('/<screen>/list', methods=['GET'])
def list_tabs(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.get('http://' + host + '/' + screen + '/tabs')
    return str(wick_req.json)

@app.route('/<screen>/details', methods=['GET'])
def tab_details(screen):
    host = _get_host_or_404(screen)

    wick_req = requests.get('http://' + host + '/' + screen + '/active_tab')
    return str(wick_req.json)

@app.route('/<screen>/show', methods=['GET'])
def show(screen):
    pass

@app.route('/<screen>/close', methods=['GET'])
def close(screen):
    pass

@app.route('/<screen>/refresh', methods=['GET'])
def refresh(screen):
    pass

@app.route('/<screen>/next', methods=['GET'])
def next(screen):
    pass

@app.route('/<screen>/previous', methods=['GET'])
def previous(screen):
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0')
