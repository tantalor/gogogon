import smtplib
import yaml
import sys
from supervisor.childutils import listener

config = yaml.load(file('conf/listener.yaml', 'r'))

while 1:
  (header, payload) = listener.wait()
  if "processname:gogogon-consumer" in payload:
    server = smtplib.SMTP(config['server']['host'])
    server.starttls() 
    server.login(config['server']['username'], config['server']['password'])
    server.sendmail(config['message']['from_addr'], config['message']['to_addrs'], config['message']['body'])
    server.quit()
  listener.ok()
