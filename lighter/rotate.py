#!/usr/bin/env python

import sys
import time
import requests
from lighter import _stringify_request_uri

host = sys.argv[1]
screen = sys.argv[2]
delay = sys.argv[3]

while(True):
    wick_req = requests.post(_stringify_request_uri(host, screen, 'next_tab'))
    # lock the screen
    wick_req = requests.post(_stringify_request_uri(host, screen, 'lock'))
    time.sleep(int(delay))
    # unlock the screen
    wick_req = requests.post(_stringify_request_uri(host, screen, 'lock'))
