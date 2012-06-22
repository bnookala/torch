import json
import requests

from flask import Flask, request

import browser
import config

app = Flask(__name__)

def _register_prefix():
	"Tell the lighter host what screens this wick controls."
	requests.post('http://' + config.lighter_host + '/register_prefix', {
		'prefix': config.screen_name_prefix,
		'port': config.port,
	})

def browser_action(fn, screen, *args):
	if screen not in browser.locked_screens:
		"To save some typing. args are expected params in the request."
		fn(screen, *(request.form[arg] for arg in args))
		return 'ok'
	else:
		return '%s is currently locked' % screen

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

@app.route('/<screen>/fullscreen_on', methods=['POST'])
def fullscreen_on(screen):
	browser.presentation_mode(screen, True)
	return 'ok'

@app.route('/<screen>/fullscreen_off', methods=['POST'])
def fullscreen_off(screen):
	browser.presentation_mode(screen, False)
	return 'ok'

@app.route('/<screen>/execute', methods=['POST'])
def execute(screen):
	return browser_action(browser.execute_script, screen, 'script')

@app.route('/<screen>/lock', methods=['POST'])
def toggle_screen(screen):
	return browser.toggle_screen(screen)

@app.route('/enumerate', methods=['GET'])
def enumerate_screens():
	return json.dumps(browser.enumerate_screens())

@app.route('/list', methods=['GET'])
def list_screens():
	return json.dumps(browser.list_screens())

if __name__ == "__main__":
	_register_prefix()
	app.run(host='0.0.0.0', port=config.port, debug=True)
