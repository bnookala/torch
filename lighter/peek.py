#!/usr/bin/env python

import sys
import time
import requests
from lighter import _stringify_request_uri, _get_y_url

host = sys.argv[1]
screen = sys.argv[2]
url = sys.argv[3]
duration = sys.argv[4]

# do something
new_url = _get_y_url(url)
if not new_url:
    new_url = url

wick_req = requests.post(_stringify_request_uri(host, screen, 'new_tab'), data={'url': new_url})
# Lock the screen.
wick_req = requests.post(_stringify_request_uri(host, screen, 'lock')
time.sleep(int(duration))
# Unlock the screen.
wick_req = requests.post(_stringify_request_uri(host, screen, 'lock')
wick_req = requests.post(_stringify_request_uri(host, screen, 'close_tab'))

