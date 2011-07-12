#!/usr/bin/python

import os
import sys
import json
import logging
import logging.handlers
import signal
import pycurl

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
  
  signal.signal(signal.SIGINT, shutdown)
  
  def recv(line):
    if line.strip():
      data = json.loads(line)
      globalhash = data.get('g')
      url = data.get('u')
      logger.info("%s %s" % (globalhash, url))

  logger.debug("starting up")
  curl = pycurl.Curl()
  curl.setopt(pycurl.URL, "http://bitly.measuredvoice.com/usa.gov")  
  curl.setopt(pycurl.WRITEFUNCTION, recv)  
  curl.perform()

def shutdown(*args):
  global logger, curl
  
  logger.debug("shutting down")
  sys.exit(-1)

if __name__ == '__main__':
  main()
