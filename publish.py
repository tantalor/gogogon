#!/usr/bin/python

import datetime
import os
import sys
import subprocess

def main():
  today = datetime.datetime.today()
  one_day = datetime.timedelta(1)
  yesterday = today - one_day
  
  logfile = "/var/log/gogogon/consumer.log.%04d-%02d-%02d" % \
    (yesterday.year, yesterday.month, yesterday.day)
  
  if not os.path.exists(logfile): return
  
  cmd = 'grep INFO %s | cut -f 4 -d " " | sort | uniq -c' % logfile
  pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  
  for line in pipe.stdout:
    (count, global_hash) = line.strip().split()
    print (count, global_hash)

if __name__ == '__main__':
  main()
