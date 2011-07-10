#!/usr/bin/python

import os
import sys
import json
import logging
import logging.handlers
import signal
import subprocess

def main():
  global logger, curl
  
  formatter = logging.Formatter('%(process)d %(levelname)s %(created)d %(message)s', '%Y-%m-%d %H:%M:%S')

  handler = logging.handlers.TimedRotatingFileHandler(
    '/var/log/gogogon/consumer.log', 'midnight', 1, backupCount=3
  )
  handler.setFormatter(formatter)

  logger = logging.getLogger()
  logger.addHandler( handler )
  logger.setLevel(logging.DEBUG)
  
  logger.debug("starting up")
  cmd = ("curl", "--no-buffer", "-s", "http://bitly.measuredvoice.com/usa.gov")
  curl = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  
  signal.signal(signal.SIGINT, shutdown)
  
  while 1:
    line = curl.stdout.readline().lstrip()
    if line:
      data = json.loads(line)
      globalhash = data.get('g')
      url = data.get('u')
      logger.info("%s %s" % (globalhash, url))

def shutdown(*args):
  global logger, curl
  
  logger.debug("shutting down")
  curl.terminate()

if __name__ == '__main__':
  main()
