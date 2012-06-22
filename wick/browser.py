import applescripts

def _screen_index(screen_name):
	#TODO
	return 1

def new_tab(screen, url):
	applescripts.run_script(applescripts.NEW_TAB % {
		'window': _screen_index(screen),
		'url': url,
	})

def get_tab_urls(screen):
	"Return a dict mapping tab index to tab url. Indices start at 1 due to Chrome's AppleScript interface."
	url_lines = applescripts.run_script(applescripts.GET_TAB_URLS % {
		'window': _screen_index(screen),
	})
	# Last 2 lines returned by GET_TAB_URLS will be newlines
	url_lines = url_lines.split('\n')[:-2]
	return dict(zip(range(1,len(url_lines)+1), url_lines))

def insert_script_in_active_tab(screen):
	return
