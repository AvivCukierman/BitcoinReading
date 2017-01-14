#!/usr/bin/env python

import sys
sys.path.append('PythonPusherClient')

import time
from datetime import datetime

import pusherclient

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

import json

global pusher

def print_usage(filename):
  print("Usage: python %s" % filename)

def channel_callback(data):
  time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
  with open('data_'+time+'.txt', 'w') as outfile:
    json.dump(data, outfile)
  print("Channel Callback: %s" % data)
  #print time


def connect_handler(data):
  channel = pusher.subscribe("order_book")

  #channel.bind('my_event', channel_callback)
  channel.bind('data', channel_callback)
  

if __name__ == '__main__':
  appkey = "de504dc5763aeef9ff52"

  pusher = pusherclient.Pusher(appkey)

  pusher.connection.bind('pusher:connection_established', connect_handler)
  #pusher.connection.bind('trade', connect_handler)
  pusher.connect()

  while True:
    time.sleep(1)
