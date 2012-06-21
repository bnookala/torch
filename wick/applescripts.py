from subprocess import Popen, PIPE, STDOUT

CHANGE_TAB_INDEX = """
tell application "Google Chrome"
	set active tab index of first window to %(index)s
end tell
"""

NEW_TAB = """
tell application "Google Chrome"
	set myTab to make new tab at end of tabs of window 1
	set URL of myTab to "%(url)s"
end tell
"""

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
