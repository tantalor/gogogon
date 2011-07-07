#!/usr/bin/python

import os
import json
import logging
import logging.handlers
import daemon
import lockfile

def main():
  formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')
  
  handler = logging.handlers.TimedRotatingFileHandler(
    '/var/log/gogogon/consumer.log', 'midnight', 1, backupCount=3
  )
  handler.setFormatter(formatter)
  
  logger = logging.getLogger()
  logger.addHandler( handler )
  logger.setLevel(logging.INFO)
  
  fh = os.popen("curl --no-buffer -s http://bitly.measuredvoice.com/usa.gov")
  while 1:
    line = fh.readline().lstrip()
    if line:
      data = json.loads(line)
      globalhash = data.get('h')
      logger.info(globalhash)

context = daemon.DaemonContext()
with context:
  main()
