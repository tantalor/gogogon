#!/usr/bin/env python

import datetime
import os
import sys
import subprocess
import bitly
from domain import domain
import json
import csv
import optparse
from csv_unicode_writer import UnicodeWriter

GROUPSIZE = 10
LOG_INPUT_DIR = "/var/log/gogogon"
LOG_INPUT_PREFIX = os.path.join(LOG_INPUT_DIR, "consumer.log")
RANKS_OUTPUT_DIR = os.path.join(LOG_INPUT_DIR, "ranks")

def main():
  today = datetime.datetime.today()
  one_day = datetime.timedelta(1)
  yesterday = today - one_day
  ymd = "%04d-%02d-%02d" % (yesterday.year, yesterday.month, yesterday.day)
  
  # find yesterday's log
  logfile = os.path.join(LOG_INPUT_DIR, "consumer.log.%s" % ymd)
  # But allow this to be overridden
  parser = optparse.OptionParser()
  parser.add_option('-f', '--file', dest="logfile", 
                    default=logfile)
  parser.add_option('-o', '--output-directory', dest="output_dir", 
                    default= RANKS_OUTPUT_DIR)
  parser.add_option('-a', '--agency', dest="use_agency_domain", 
                    default=False)
  options, remainder = parser.parse_args()
  logfile = options.logfile
  output_dir = options.output_dir
            
  if not os.path.exists(logfile): 
      raise RuntimeError('Log file does not exist: ' + logfile)
  if not os.path.exists(output_dir):
      raise RuntimeError('Output directory does not exist: ' + output_dir)
  
  # sort and uniq the log
  cmd = 'grep INFO %s | cut -f 4- -d " " | sort | uniq -c' % logfile
  pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  
  # collect up global hashes and click counts
  details = dict()
  for line in pipe.stdout:
    (count, global_hash, url) = line.strip().split(' ', 2)
    details[global_hash] = dict(
      u=url,
      global_clicks=long(count),
      agency=domain(url),
      global_hash=global_hash,
    )
  
  # grab hashes in groups of GROUPSIZE size
  for i in xrange(1+len(details)/GROUPSIZE):
    hashes = details.keys()[i*GROUPSIZE:i*GROUPSIZE+GROUPSIZE]
    # lookup titles
    for item in bitly.info(hashes=hashes):
      if 'title' not in item: continue
      details[item['hash']]['title']=item['title']
    # lookup yesterday's clicks
    for item in bitly.clicks_by_day(hashes=hashes, days=2):
      if 'clicks' not in item: continue
      clicks = int(item['clicks'][1]['clicks'])
      if clicks > details[item['hash']]['global_clicks']:
        details[item['hash']]['global_clicks'] = clicks
  
  # sort by global clicks descending
  records = details.values()
  records.sort(key=lambda x: x["global_clicks"], reverse=True)  

  write_output_files(records, ymd, output_dir)
  if options.use_agency_domain:
    write_agency_domain_files(records, output_dir, ymd)

def write_output_files(records, ymd, output_dir=RANKS_OUTPUT_DIR, latest=True):

  # output files
  json_file = os.path.join(output_dir, "%s.json" % ymd)
  csv_file = os.path.join(output_dir, "%s.csv" % ymd)
  json_latest_file = os.path.join(output_dir, "latest.json")

  # write json
  json.dump(records, file(json_file, 'w'))
  if latest:
    json.dump(records[:10], file(json_latest_file, 'w'))
  
  # write csv
  csv_writer = UnicodeWriter(file(csv_file, 'w'))
  csv_writer.writerow(["Long URL", "Page Title", "Clicks", "Agency Domain", "Global hash"])
  for record in records:
    if not 'title' in record or not record['title']: continue
    url = record['u'] if type(record['u']) == unicode else record['u'].decode('utf8')
    csv_writer.writerow([
      url,
      record['title'],
      str(record['global_clicks']),
      record['agency'],
      record['global_hash'],
    ])


def write_agency_domain_files(records, output_dir, ymd):
  domains = dict()
  for record in records:
    domain = domains.setdefault(record['agency'],
                                dict(agency=record['agency'], global_clicks=0))
    domain['global_clicks'] = domain['global_clicks'] + record['global_clicks']

  domain_records = domains.values()
  domain_records.sort(key=lambda x: x["global_clicks"], reverse=True)  

  json_file = os.path.join(output_dir, "domain-%s.json" % ymd)
  csv_file = os.path.join(output_dir, "domain-%s.csv" % ymd)
  json_latest_file = os.path.join(output_dir, "latest-domain.json")

  # write json
  json.dump(domain_records, file(json_file, 'w'))
  json.dump(domain_records[:10], file(json_latest_file, 'w'))

  # write csv
  csv_writer = csv.writer(file(csv_file, 'w'))
  csv_writer.writerow(["Agency Domain", "Clicks"])
  for record in domain_records:
    if not 'agency' in record: continue
    csv_writer.writerow([
      record['agency'],
      record['global_clicks'],
    ])

if __name__ == '__main__':
  main()
