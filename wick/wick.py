from flask import Flask, request

import applescripts

app = Flask(__name__)

@app.route('/restart', methods=['POST'])
def restart():
	applescripts.run_script(applescripts.RESTART_CHROME)
	return 'ok'

@app.route('/new_tab', methods=['POST'])
def new_tab():
	applescripts.run_script(applescripts.NEW_TAB % {'url': request.form['url']})
	return 'ok'

if __name__ == "__main__":
	app.run()
