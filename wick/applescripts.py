from subprocess import Popen, PIPE, STDOUT

CHANGE_TAB_INDEX = """
tell application "Google Chrome"
	set active tab index of first window to %(index)s
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
	tell tab %(tab)s of window %(window)s of application "Google Chrome" to reload
end tell
"""

CLOSE_TAB = """
tell application "Google Chrome"
	tell tab %(tab)s of window %(window)s of application "Google Chrome" to close
end tell
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
		set res to res & (URL of tab i of window %(window)s) & " " & (title of tab i of window 1) & "
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

def run_script(script):
	p = Popen('osascript', stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	result = p.communicate(input=script)[0]
	print result
	return result
