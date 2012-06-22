import json

from flask import Flask, request

import browser

app = Flask(__name__)

def browser_action(fn, screen, *args):
	"To save some typing. args are expected params in the request."
	fn(screen, *(request.form[arg] for arg in args))
	return 'ok'

@app.route('/<screen>/tabs', methods=['GET'])
def tabs(screen):
	return json.dumps(browser.get_tab_info(screen))

@app.route('/<screen>/active_tab', methods=['GET'])
def active_tab(screen):
	return json.dumps(browser.get_active_tab(screen))

@app.route('/<screen>/restart', methods=['POST'])
def restart(screen):
	return browser_action(browser.restart_chrome, screen)

@app.route('/<screen>/new_tab', methods=['POST'])
def new_tab(screen):
	browser.new_tab(screen, request.form['url'])
	return json.dumps(browser.get_tab_info(screen))

@app.route('/<screen>/activate_tab', methods=['POST'])
def activate_tab(screen):
	return browser_action(browser.activate_tab, screen, 'index')

@app.route('/<screen>/reload', methods=['POST'])
def reload(screen):
	return browser_action(browser.reload_tab, screen)

@app.route('/<screen>/close_tab', methods=['POST'])
def close_tab(screen):
	return browser_action(browser.close_tab, screen)

@app.route('/<screen>/next_tab', methods=['POST'])
def next_tab(screen):
	return browser_action(browser.next_tab, screen)

@app.route('/<screen>/prev_tab', methods=['POST'])
def prev_tab(screen):
	return browser_action(browser.prev_tab, screen)

@app.route('/<screen>/presentation_mode_on', methods=['POST'])
def presentation_mode_on(screen):
	browser.presentation_mode(screen, True)
	return 'ok'

@app.route('/<screen>/presentation_mode_off', methods=['POST'])
def presentation_mode_off(screen):
	browser.presentation_mode(screen, False)
	return 'ok'

@app.route('/<screen>/execute', methods=['POST'])
def execute(screen):
	return browser_action(browser.execute_script, screen, 'script')

@app.route('/enumerate', methods=['POST'])
def enumerate_tabs():
	return json.dumps(browser.enumerate_tabs())

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
