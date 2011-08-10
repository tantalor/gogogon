#!/usr/bin/env python

import os
import sys
import json
import logging
import logging.handlers
import signal
import pycurl
import optparse

def main():
  global logger
  
  parser = optparse.OptionParser()
  parser.add_option('-f', '--file', dest="use_log_file", 
                    default='/var/log/gogogon/consumer.log')
  options, remainder = parser.parse_args()
  log_file = options.use_log_file
    
  formatter = logging.Formatter('%(process)d %(levelname)s %(created)d %(message)s', '%Y-%m-%d %H:%M:%S')

  handler = logging.handlers.TimedRotatingFileHandler(
    log_file, 'midnight', 1, backupCount=3
  )
  handler.setFormatter(formatter)

  logger = logging.getLogger()
  logger.addHandler( handler )
  logger.setLevel(logging.DEBUG)
  
  signal.signal(signal.SIGINT, shutdown)
  
  def recv(line):
    if line.strip():
      (globalhash, url) = get_fields(line)
      logger.info("%s %s" % (globalhash, url))

  logger.debug("starting up")
  curl = pycurl.Curl()
  curl.setopt(pycurl.URL, "http://bitly.measuredvoice.com/usa.gov")  
  curl.setopt(pycurl.WRITEFUNCTION, recv)  
  curl.perform()

def get_fields(line):  
  data = json.loads(line)
  globalhash = data.get('g')
  url = data.get('u')
  return (globalhash, url)

def shutdown(*args):
  global logger

  logger.debug("shutting down")
  logger.flush()
  sys.exit()

if __name__ == '__main__':
  main()
