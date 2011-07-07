#!/usr/bin/python

import os
import json
import logging
import logging.handlers

formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S')

handler = logging.handlers.TimedRotatingFileHandler('consumer.log', 'midnight', 1, backupCount=3)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler( handler )
logger.setLevel(logging.INFO)

def main():
  fh = os.popen("curl --no-buffer -s http://bitly.measuredvoice.com/usa.gov")
  while 1:
    line = fh.readline().lstrip()
    if line:
      data = json.loads(line)
      globalhash = data.get('h')
      logger.info(globalhash)

if __name__ == '__main__':
  main()
