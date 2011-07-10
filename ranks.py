#!/usr/bin/python

import datetime
import os
import sys
import subprocess
import bitly
from domain import domain
import json

GROUPSIZE = 10

def main():
  today = datetime.datetime.today()
  one_day = datetime.timedelta(1)
  yesterday = today - one_day
  
  # find yesterday's log
  logfile = "/var/log/gogogon/consumer.log.%04d-%02d-%02d" % \
    (yesterday.year, yesterday.month, yesterday.day)
  if not os.path.exists(logfile): return
  
  # sort and uniq the log
  cmd = 'grep INFO %s | cut -f 4-5 -d " " | sort | uniq -c' % logfile
  pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  
  # collect up global hashes and click counts
  details = dict()
  for line in pipe.stdout:
    (count, global_hash, url) = line.strip().split()
    details[global_hash] = dict(
      u=url,
      global_clicks=count,
      agency=domain(url),
      global_hash=global_hash,
    )
  
  # grab hashes in groups of GROUPSIZE size
  for i in xrange(1+len(details)/GROUPSIZE):
    hashes = details.keys()[i*GROUPSIZE:i*GROUPSIZE+GROUPSIZE]
    # lookup titles
    for info in bitly.info(*hashes):
      details[info['hash']]['title']=info['title']
  
  print "\n".join(json.dumps(d) for d in details.values())

if __name__ == '__main__':
  main()
