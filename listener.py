#!/usr/bin/env python

import smtplib
import yaml
import sys
from supervisor.childutils import listener
import os

localdir = os.path.dirname(__file__)
config_file = os.path.join(localdir, 'conf', 'listener.yaml')
config = yaml.load(file(config_file, 'r'))

while 1:
  (header, payload) = listener.wait()
  if "processname:gogogon-consumer" in payload:
    server = smtplib.SMTP(config['server']['host'])
    server.starttls() 
    server.login(config['server']['username'], config['server']['password'])
    server.sendmail(config['message']['from_addr'], config['message']['to_addrs'], config['message']['body'])
    server.quit()
  listener.ok()
