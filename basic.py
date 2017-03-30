#!/usr/bin/env python

import sys
sys.path.append('PythonPusherClient')
import os

import time
import pusherclient
import json

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--stream", dest="stream",help="which stream to store")
parser.add_option("-t", "--time_diff", dest="time_diff",help="how long before saving", type=int, default=5)
parser.add_option("-q", "--quiet",action="store_true", dest="quiet", default=False,help="don't print things")
(opts, args) = parser.parse_args()

if opts.stream not in ['order_book','live_trades','diff_order_book']:
  raise RuntimeError('Not a valid stream.')
if opts.stream=='order_book':
  opts.appkey = 'de504dc5763aeef9ff52' 
  opts.event = 'data'
  opts.submitDir = 'order_book'
if opts.stream=='live_trades':
  opts.appkey = 'de504dc5763aeef9ff52' 
  opts.event = 'trade'
  opts.submitDir = 'ticker'
if opts.stream=='diff_order_book':
  opts.appkey = 'de504dc5763aeef9ff52' 
  opts.event='data'
  opts.submitDir = 'diff_order_book'

if not os.path.exists(opts.submitDir):
  print '== Making folder \''+opts.submitDir+'\' =='
  os.makedirs(opts.submitDir)

global pusher

def print_usage(filename):
  print("Usage: python %s" % filename)

import pickle
#import pdb
#import numpy

def channel_callback(data):
  print("Channel Callback: %s" % data)

  timestamp = int(time.time())
  #print timestamp,d['timestamp'] #they're the same
  timestamp_rounded = timestamp-timestamp%time_diff #rounded to nearest time_diff seconds
  if timestamp_rounded not in bigdict: bigdict[timestamp_rounded] = []

  d = json.loads(data)
  if opts.stream=='order_book':
    d['timestamp'] = str(timestamp)
  if opts.stream=='order_book' or opts.stream=='diff_order_book':
    newdict = {k:0 for k in d.keys()}
    for k in d.keys():
      if k=='timestamp': newdict[k] = int(d[k])
      else:
        newarr = []
        for val in d[k]:
          newarr.append([float(val[0]),float(val[1])])
        newdict[k] = newarr
    bigdict[timestamp_rounded].append(newdict)
  else:
    bigdict[timestamp_rounded].append(newdict)

def connect_handler(data):
  channel = pusher.subscribe(opts.stream)
  channel.bind(opts.event, channel_callback)

  
from suppress_stdout import suppress_stdout_stderr
if __name__ == '__main__':
  #completely suppress output
  if opts.quiet:
    print 'Suppressing all stdout!'
  with suppress_stdout_stderr(quiet=opts.quiet):
      #dict every so often
      time_diff = opts.time_diff
      timestamp = int(time.time())
      timestamp_rounded = timestamp-timestamp%time_diff #rounded to nearest time_diff seconds
      bigdict = {timestamp_rounded:[]}

      pusher = pusherclient.Pusher(opts.appkey)

      pusher.connection.bind('pusher:connection_established', connect_handler)
      #pusher.connection.bind('trade', connect_handler)
      pusher.connect()

      while True:
        time.sleep(time_diff*2)
        timestamp = int(time.time())
        timestamp_rounded = timestamp-timestamp%time_diff #rounded to nearest 10 seconds
        keys = bigdict.keys()
        for k in keys:
          if k<timestamp_rounded:
              print 'Saving data'
              print len(bigdict)
              with open(opts.submitDir+'/data_'+str(k)+'.p', 'wb') as outfile:
                pickle.dump(bigdict[k], outfile, protocol=pickle.HIGHEST_PROTOCOL)
              del bigdict[k]
