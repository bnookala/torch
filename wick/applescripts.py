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

def run_script(script):
	p = Popen('osascript', stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = p.communicate(input=script)[0]
	print result
	return result
