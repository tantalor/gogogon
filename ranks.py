#!/usr/bin/python

import datetime
import os
import sys
import subprocess
import bitly
from domain import domain
import json
import csv

GROUPSIZE = 10
LOG_INPUT_DIR = "/var/log/gogogon"
RANKS_OUTPUT_DIR = os.path.join(LOG_INPUT_DIR, "ranks")

def main():
  today = datetime.datetime.today()
  one_day = datetime.timedelta(1)
  yesterday = today - one_day
  ymd = "%04d-%02d-%02d" % (yesterday.year, yesterday.month, yesterday.day)
  
  # find yesterday's log
  logfile = os.path.join(LOG_INPUT_DIR, "consumer.log.%s" % ymd)
  if not os.path.exists(logfile): return
  
  # sort and uniq the log
  cmd = 'grep INFO %s | cut -f 4- -d " " | sort | uniq -c' % logfile
  pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  
  # collect up global hashes and click counts
  details = dict()
  for line in pipe.stdout:
    (count, global_hash, url) = line.strip().split(' ', 2)
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
    for item in bitly.info(hashes=hashes):
      if not item['title']: continue
      details[item['hash']]['title']=item['title']
    # lookup yesterday's clicks
    for item in bitly.clicks_by_day(hashes=hashes, days=2):
      clicks = item['clicks'][1]['clicks']
      if clicks > details[item['hash']]['global_clicks']:
        details[item['hash']]['global_clicks'] = clicks
  
  # output files
  json_file = os.path.join(RANKS_OUTPUT_DIR, "%s.json" % ymd)
  csv_file = os.path.join(RANKS_OUTPUT_DIR, "%s.csv" % ymd)
  json_latest_file = os.path.join(RANKS_OUTPUT_DIR, "latest.json")
  
  # sort by global clicks descending
  records = details.values()
  records.sort(key=lambda x: x["global_clicks"], reverse=True)  

  # write json
  json.dump(records, file(json_file, 'w'))
  json.dump(records[:10], file(json_latest_file, 'w'))
  
  # write csv
  csv_writer = csv.writer(file(csv_file, 'w'))
  csv_writer.writerow(["Long URL", "Page Title", "Clicks", "Agency Domain", "Global hash"])
  for record in records:
    if not 'title' in record: continue
    csv_writer.writerow([
      record['u'],
      record['title'].encode('utf8'),
      record['global_clicks'],
      record['agency'],
      record['global_hash'],
    ])

if __name__ == '__main__':
  main()
