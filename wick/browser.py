import applescripts

def _screen_index(screen_name):
	"Convert a screen name like consumer1 into its window index for AppleScript"
	#TODO
	return 1

def restart_chrome(screen):
	applescripts.run_script(applescripts.RESTART_CHROME)

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

def reload_tab(screen, index):
	applescripts.run_script(applescripts.RELOAD_TAB % {
		'window': _screen_index(screen),
		'tab': index,
	})

def close_tab(screen, index):
	applescripts.run_script(applescripts.CLOSE_TAB % {
		'window': _screen_index(screen),
		'tab': index,
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
	index, url, title = info.split(' ', 2)
	return {'index': int(index), 'url': url, 'title': title}

def get_tab_info(screen):
	"Return a dict mapping tab index to tab url. Indices start at 1 due to Chrome's AppleScript interface."
	tab_lines = applescripts.run_script(applescripts.GET_TAB_INFO % {
		'window': _screen_index(screen),
	})
	# Last 2 lines returned will be newlines
	tab_lines = tab_lines.split('\n')[:-2]
	# Convert space-delimited urls and titles
	result = {}
	for index, line in enumerate(tab_lines):
		url, title = line.split(' ', 1)
		result[index + 1] = {'url': url, 'title': title}
	return result
