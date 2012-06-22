import json

from flask import Flask, request

import applescripts
import browser

app = Flask(__name__)

@app.route('/execute', methods=['POST']):
	script = request.form['script']
	return 'ok'

@app.route('/enumerate', methods=['POST'])
def enumerate():
	return 'ok'

@app.route('/<screen>/tabs', methods=['GET'])
def tabs(screen):
	return json.dumps(browser.get_tab_urls(screen))

@app.route('/<screen>/restart', methods=['POST'])
def restart(screen):
	applescripts.run_script(applescripts.RESTART_CHROME)
	return 'ok'

@app.route('/<screen>/show', methods=['POST'])
def show(screen):
	# will be a tab index or url
	to_show = request.form['to_show']
	print to_show
	for index, url in browser.get_tab_urls(screen).iteritems():
		if to_show in url:
			#TODO activate tab #index
			break
	browser.new_tab(screen, to_show)
	return 'ok'

@app.route('/<screen>/reload', methods=['POST'])
def reload(screen):
	return 'ok'

@app.route('/<screen>/next_tab', methods=['POST'])
def next_tab(screen):
	return 'ok'

@app.route('/<screen>/prev_tab', methods=['POST'])
def prev_tab(screen):
	return 'ok'

@app.route('/<screen>/close_tab', methods=['POST'])
def close_tab(screen):
	return 'ok'

if __name__ == "__main__":
	app.run(host='0.0.0.0')
