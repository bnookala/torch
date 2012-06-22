from flask import Flask, request
app = Flask(__name__)

@app.route('/list', methods=['GET'])
def list():
    pass

@app.route('/enumerate', methods=['GET'])
def enumerate():
    pass

@app.route('/<screen>/list', methods=['GET'])
def list_tabs(screen):
    pass

@app.route('/<screen>/details', methods=['GET'])
def tab_details(screen):
    pass

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
