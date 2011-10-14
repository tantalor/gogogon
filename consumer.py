#!/usr/bin/env python

import os
import sys
import anyjson
import logging
import logging.handlers
import signal
import pycurl
import optparse

def main():
  parser = optparse.OptionParser()
  parser.add_option('-f', '--file', dest="use_log_file", 
                    default='/var/log/gogogon/consumer.log')
  options, remainder = parser.parse_args()
  log_file = options.use_log_file
    
  formatter = logging.Formatter('%(process)d %(levelname)s %(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')

  handler = logging.handlers.TimedRotatingFileHandler(
    log_file, 'midnight', 1, backupCount=3
  )
  handler.setFormatter(formatter)

  logger = logging.getLogger()
  logger.addHandler( handler )
  logger.setLevel(logging.DEBUG)
  logger.debug("starting up")
  
  def shutdown(*args):
    logger.debug("shutting down")
    sys.exit()
  
  signal.signal(signal.SIGINT, shutdown)
  
  def recv(line):
    if line.strip():
      (globalhash, url) = get_fields(line)
      logger.info("%s %s" % (globalhash, url))

  while 1:
    try:
      logger.debug("starting pycurl")
      curl = pycurl.Curl()
      curl.setopt(pycurl.URL, "http://bitly.measuredvoice.com/usa.gov")  
      curl.setopt(pycurl.WRITEFUNCTION, recv)  
      curl.perform()
    except Exception, e:
      logger.error(e)

def get_fields(line):  
  data = anyjson.deserialize(line)
  globalhash = data.get('g')
  url = data.get('u')
  return (globalhash, url)

if __name__ == '__main__':
  main()
