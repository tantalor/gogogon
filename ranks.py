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

GROUPSIZE = 10
file_name_prefix = "/var/log/gogogon/consumer.log"
default_output_directory = "/var/log/gogogon/ranking"

def main():
  today = datetime.datetime.today()
  one_day = datetime.timedelta(1)
  yesterday = today - one_day
  iso_date = "%04d-%02d-%02d" % \
    (yesterday.year, yesterday.month, yesterday.day)
  # Use yesterday's log by default
  logfile = file_name_prefix + "." + iso_date

  # But allow this to be overridden
  parser = optparse.OptionParser()
  parser.add_option('-f', '--file', dest="logfile", 
                    default=logfile)
  parser.add_option('-o', '--output-directory', dest="output_directory", 
                    default= default_output_directory)
  parser.add_option('-a', '--agency', dest="use_agency_domain", 
                    default=False)
  options, remainder = parser.parse_args()
  logfile = options.logfile
  output_directory = options.output_directory
            
  if not os.path.exists(logfile): 
      raise RuntimeError('Log file does not exist: ' + logfile)
  if not os.path.exists(output_directory):
      raise RuntimeError('Output directory does not exist: ' + output_directory)
  
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
    for info in bitly.info(*hashes):
      if not info['title']: continue
      details[info['hash']]['title']=info['title']
  
  # output files
  json_file = output_directory + "/" + iso_date + ".json"
  csv_file = output_directory + "/" + iso_date + ".csv"

  
  # sort by global clicks descending
  records = details.values()
  records.sort(key=lambda x: x["global_clicks"], reverse=True)  


  # write json
  json.dump(records, file(json_file, 'w'))
  
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

  if options.use_agency_domain:
    write_agency(records, output_directory, iso_date)


def write_agency(records, output_directory, iso_date):
  domains = dict()
  for record in records:
    domain = domains.setdefault(record['agency'],
                                dict(agency=record['agency'], global_clicks=0))
    domain['global_clicks'] = domain['global_clicks'] + record['global_clicks']

  domain_records = domains.values()
  domain_records.sort(key=lambda x: x["global_clicks"], reverse=True)  

  json_file = output_directory + "/domain-" + iso_date + ".json"
  csv_file = output_directory + "/domain-" + iso_date + ".csv"

  # write json
  json.dump(domain_records, file(json_file, 'w'))

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
