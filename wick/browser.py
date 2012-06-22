import applescripts
import config
import javascripts

#TODO make this not a stupid global
ids_to_screen_names = None

def _refresh_ids():
	"Track the ids of all the open browser windows."
	global ids_to_screen_names
	ids_to_screen_names = {}
	ids_and_bounds = applescripts.run_script(applescripts.GET_WINDOW_IDS_AND_BOUNDS)
	ids_and_bounds = ids_and_bounds.strip().split('\n')
	ids_and_bounds = [line.strip().split(' ') for line in ids_and_bounds]
	# sort by distance from top left, with more weight on y
	comp = lambda line: int(line[1]) ** 2 + int(line[2]) ** 3
	for i, line in enumerate(sorted(ids_and_bounds, key=comp)):
		screen_name = config.screen_name_prefix + str(i + 1)
		ids_to_screen_names[line[0]] = screen_name

def _screen_index(screen_name):
	"""
	Convert a screen name like consumer1 into its window index for AppleScript.
	We have a mapping of name->id but AppleScript seems to index only by window index.
	"""
	global ids_to_screen_names
	if not ids_to_screen_names:
		_refresh_ids()
	num_windows = int(applescripts.run_script(applescripts.GET_NUM_WINDOWS))
	for i in xrange(1, num_windows + 1):
		id = applescripts.run_script(applescripts.GET_WINDOW_ID_FROM_INDEX % {'window': i}).strip()
		if ids_to_screen_names.get(id) == screen_name:
			return i

	raise Exception("Screen name %s not found" % screen_name)

def restart_chrome(screen):
	applescripts.run_script(applescripts.RESTART_CHROME)

def presentation_mode(screen, toggle):
	applescripts.run_script(applescripts.PRESENTATION_MODE % {
		'window': _screen_index(screen),
		'enter_or_exit': 'enter' if toggle else 'exit',
	})

def new_tab(screen, url):
	applescripts.run_script(applescripts.NEW_TAB % {
		'window': _screen_index(screen),
		'url': url,
	})

def activate_tab(screen, index):
	applescripts.run_script(applescripts.ACTIVATE_TAB % {
		'window': _screen_index(screen),
		'tab': index,
	})

def reload_tab(screen):
	applescripts.run_script(applescripts.RELOAD_TAB % {
		'window': _screen_index(screen),
	})

def close_tab(screen):
	applescripts.run_script(applescripts.CLOSE_TAB % {
		'window': _screen_index(screen),
	})

def next_tab(screen):
	num_tabs = len(get_tab_info(screen))
	active_index = get_active_tab(screen)['index']
	activate_tab(screen, 1 if active_index == num_tabs else active_index + 1)

def prev_tab(screen):
	num_tabs = len(get_tab_info(screen))
	active_index = get_active_tab(screen)['index']
	activate_tab(screen, num_tabs if active_index == 1 else active_index - 1)

def get_active_tab(screen):
	info = applescripts.run_script(applescripts.GET_ACTIVE_TAB % {
		'window': _screen_index(screen),
	})
	index, url = info.strip().split(' ', 1)
	url, title = url.split(' ', 1) if ' ' in url else (url, url)
	return {'index': int(index), 'url': url, 'title': title}

def get_tab_info(screen):
	"Return a dict mapping tab index to tab url. Indices start at 1 due to Chrome's AppleScript interface."
	tab_lines = applescripts.run_script(applescripts.GET_TAB_INFO % {
		'window': _screen_index(screen),
	})
	tab_lines = tab_lines.strip().split('\n')
	# Convert space-delimited urls and titles
	result = {}
	for index, line in enumerate(tab_lines):
		url, title = line.split(' ', 1) if ' ' in line else (line, line)
		result[index + 1] = {'url': url, 'title': title}
	return result

def execute_script(screen, script, by_url=False):
	applescripts.run_script(applescripts.EXECUTE_SCRIPT % {
		'window': _screen_index(screen),
		'script': script.replace('"', '\\"').replace('\n',''),
	})

def show_big_text(screen, text):
	# ugh i feel so so dirty
	execute_script(screen, javascripts.SHOW_BIG_TEXT % {'text': text.replace('"', '\\"')})

def list_screens():
	global ids_to_screen_names
	_refresh_ids()
	return sorted(ids_to_screen_names.values())

def enumerate_screens():
	names = list_screens()
	for name in names:
		show_big_text(name, name)
	return names

def inject_nyanwin(screen, lighter_host):
	applescripts.run_script(applescripts.INJECT_NYANWIN % {
		'window': _screen_index(screen),
		'nyanwinDoneUrl': 'http://' + lighter_host + ':5000/nyanwin_done?screen=' + screen,
	})
