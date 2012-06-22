from chrome import ChromeClient
import requests
import config

r = requests.get('http://localhost:' + str(config.debugger_port) + '/json')

ws = ChromeClient(r.json[0]['webSocketDebuggerUrl'])
ws.navigate('http://www.google.com')
ws.evaluate("alert('omg')")
