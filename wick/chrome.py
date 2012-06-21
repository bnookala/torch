import config
import json
import requests
from websocket import create_connection

class ChromeClient:
     ws = None

     def __init__(self, web_socket_uri):
          self.ws = create_connection(web_socket_uri)

     def navigate(self, new_url):
          request = {
               "id": 1,
               "method": "Page.navigate",
               "params": {
                    "url": new_url
               }
          }
          request_str = json.dumps(request)
          self.ws.send(request_str)
          recv_msg = self.ws.recv()
          print recv_msg

     def evaluate(self, javascript):
          request = {
               "id": 1,
               "method": "Runtime.evaluate",
               "params": {
                    "expression": javascript,
               }
          }
          request_str = json.dumps(request)
          self.ws.send(request_str)
          recv_msg = self.ws.recv()
          print recv_msg

r = requests.get('http://localhost:' + str(config.debugger_port) + '/json')

ws = ChromeClient(r.json[0]['webSocketDebuggerUrl'])
ws.navigate('http://www.google.com')
ws.evaluate("alert('omg')")
