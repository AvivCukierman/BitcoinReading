#!/usr/bin/env python

import sys
sys.path.append('PythonPusherClient')

import time

import pusherclient

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

global pusher

def print_usage(filename):
    print("Usage: python %s <appkey>" % filename)

def channel_callback(data):
    print("Channel Callback: %s" % data)

def connect_handler(data):
    channel = pusher.subscribe("order_book")

    channel.bind('my_event', channel_callback)
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage(sys.argv[0])
        sys.exit(1)

    appkey = sys.argv[1]
    #appkey = "de504dc5763aeef9ff52"

    pusher = pusherclient.Pusher(appkey)

    pusher.connection.bind('pusher:connection_established', connect_handler)
    #pusher.connection.bind('trade', connect_handler)
    pusher.connect()

    while True:
        time.sleep(1)