#!/usr/bin/env python

import sys
import os
import re
import urllib2
import json
from domain import domain
import bitly
from datetime import date, timedelta
from ranks import write_output_files
import time
import calendar

GROUPSIZE = 10
ARCHIVE_URL = "http://bitly.measuredvoice.com/bitly_archive/"
LINK_RE = re.compile("usagov_bitly_data[\d-]*")

def date_to_epoch_seconds(d):
  return calendar.timegm(time.strptime(
    '%04d-%02d-%02d 00:00:00' % (d.year, d.month, d.day),
    '%Y-%m-%d %H:%M:%S',
  ))

def main():
  ymd = sys.argv[1]
  print "recovering %s" % ymd
  
  # gather global hashes and click counts
  details = dict()
  lines = os.popen("curl -s %s | grep %s" % (ARCHIVE_URL, ymd)).readlines()
  for line in lines:
    matches = LINK_RE.findall(line)
    if matches:
      link = ARCHIVE_URL+matches[0]
      for (global_hash, url) in read_data(link):
        if global_hash not in details:
          details[global_hash] = dict(
            u=url,
            global_clicks=1,
            agency=domain(url),
            global_hash=global_hash,
          )
        else:
          details[global_hash]['global_clicks'] += 1
  
  print "getting titles"
  # grab hashes in groups of GROUPSIZE size
  for i in xrange(1+len(details)/GROUPSIZE):
    hashes = details.keys()[i*GROUPSIZE:i*GROUPSIZE+GROUPSIZE]
    # lookup titles
    for item in bitly.info(hashes=hashes):
      if 'title' not in item: continue
      details[item['hash']]['title']=item['title']
  
  # sort by global clicks descending
  records = details.values()
  records.sort(key=lambda x: x["global_clicks"], reverse=True)  
  
  write_output_files(records=records, ymd=ymd, latest=False)

def read_data(link):     
  print link 
  lines = urllib2.urlopen(link).readlines()
  for line in lines:
    if line.strip():
      try:
        data = json.loads(line)
        global_hash = data.get('g')
        url = data.get('u')
        yield (global_hash, url)
      except ValueError, e:
        print line, e

if __name__ == '__main__':
  main()
