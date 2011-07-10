#!/usr/bin/python

import os
import sys
import json
import logging
import logging.handlers
import daemon
import lockfile
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
  
  while 1:
    line = curl.stdout.readline().lstrip()
    if line:
      data = json.loads(line)
      print data
      globalhash = data.get('g')
      url = data.get('u')
      logger.info("%s %s" % (globalhash, url))

def shutdown(*args):
  global logger, curl
  
  logger.debug("shutting down")
  curl.terminate()

signal.signal(signal.SIGINT, shutdown)

lock = lockfile.FileLock('/var/run/gogogon-consumer.pid')
if lock.is_locked(): sys.exit()

context = daemon.DaemonContext(
  pidfile=lock,
)

with context:
  main()
