from flask import Flask, request
app = Flask(__name__)

@app.route('/list', methods=['GET'])
def list():
    pass

@app.route('/enumerate', methods=['GET'])
def enumerate():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0')
