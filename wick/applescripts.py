from subprocess import Popen, PIPE, STDOUT

PRESENTATION_MODE = """
tell application "Google Chrome"
	tell window %(window)s to %(enter_or_exit)s presentation mode
end tell
"""

NEW_TAB = """
tell application "Google Chrome"
	set myTab to make new tab at end of tabs of window %(window)s
	set URL of myTab to "%(url)s"
end tell
"""

ACTIVATE_TAB = """
tell application "Google Chrome"
	set active tab index of window %(window)s to %(tab)s
end tell
"""

RELOAD_TAB = """
tell application "Google Chrome"
	tell active tab of window %(window)s of application "Google Chrome" to reload
end tell
"""

CLOSE_TAB = """
tell application "Google Chrome" to close active tab of window %(window)s
"""

BRING_WINDOW_TO_FRONT = """
tell application "Google Chrome"
	set index of window %(window)s to 1
end tell
"""

# XXX: need to toggle 'visible' property in order to focus the window to receive the keystroke
# http://stackoverflow.com/questions/5682413/how-do-i-make-a-safari-window-active-using-applescript-elegantly
ZOOM_OUT_CURRENT_WINDOW = """
tell application "Google Chrome"
	activate
	set win to window %(window)s
	tell win
		set index to 1
		set visible to false
		set visible to true
	end tell
	tell application "System Events"
		keystroke "-" using {command down}
	end tell
end tell
"""

ZOOM_IN_CURRENT_WINDOW = """
tell application "Google Chrome"
	activate
	set win to window %(window)s
	tell win
		set index to 1
		set visible to false
		set visible to true
	end tell
	tell application "System Events"
		keystroke "+" using {command down}
	end tell
end tell
"""

# Newline-delimited list of id x1 y1 x2 y2
GET_WINDOW_IDS_AND_BOUNDS = """
set res to ""
tell application "Google Chrome"
	repeat with w in windows of application "Google Chrome"
		set b to bounds of w
		set res to res & (id of w) & " " & (item 1 of b) & " " & (item 2 of b) & " " & (item 3 of b) & " " & (item 4 of b) & "
"
	end repeat
end tell
get res
"""

GET_NUM_WINDOWS = """
set c to 0
tell application "Google Chrome"
	repeat with w in windows of application "Google Chrome"
		set c to (c + 1)
	end repeat
end tell
get c
"""

GET_WINDOW_ID_FROM_INDEX = """
tell application "Google Chrome" to get id of window %(window)s
"""

# Returns '<index> <url> <title>'
GET_ACTIVE_TAB = """
tell application "Google Chrome"
	set a to active tab index of window %(window)s
	get "" & a & " " & (URL of tab a of window %(window)s) & " " & (title of tab a of window %(window)s)
end tell
"""

# Returns a newline-delimited list of '<url> <title>'
GET_TAB_INFO = """
set res to ""
tell application "Google Chrome"
	set i to 0
	repeat with t in (tabs of window %(window)s)
		set i to i + 1
		set res to res & (URL of tab i of window %(window)s) & " " & (title of tab i of window %(window)s) & "
"
	end repeat
end tell
get res
"""

# Restart Chrome in remote debugging mode
RESTART_CHROME = """
tell application "Google Chrome" to quit
tell application "Terminal"
	activate
	if exists (window 1) then
		do script "/Applications/Google\\\\ Chrome.app/Contents/MacOS/Google\\\\ Chrome --remote-debugging-port=9000" in window 1
	else
		do script "/Applications/Google\\\\ Chrome.app/Contents/MacOS/Google\\\\ Chrome --remote-debugging-port=9000"
	end if
end tell
delay 1
tell application "Google Chrome" to activate
"""

# Make sure " in the script is converted to \"
EXECUTE_SCRIPT = """
tell application "Google Chrome"
	execute active tab of window %(window)s javascript "%(script)s"
end tell
"""

INJECT_NYANWIN = """
tell application "Google Chrome"
	set URL of active tab of window %(window)s to "javascript:window.nyanwinDoneUrl='%(nyanwinDoneUrl)s';var s=document.createElement('script');s.src='http://people.yelpcorp.com/~mwilson/nyanwin.js';document.getElementsByTagName('head')[0].appendChild(s);"
end tell
"""

def run_script(script):
	p = Popen('osascript', stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = p.communicate(input=script)[0]
	print result
	return result
