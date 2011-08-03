#!/usr/bin/env python

import httplib
import urllib
import json
import unittest

API_USER = 'gogogon'
API_KEY  = 'R_cbcba050cbd86f7b2fb2a6b3e34f7c4c'

def info(hashes):
  """Yields info for each given hash."""
  response = send_to_bitly(
    url="http://api.bitly.com/v3/info",
    hashes=hashes,
  )
  if response:
    for item in response['data']['info']:
      yield item

def clicks_by_day(hashes, days=5):
  """Yields daily clicks for each given hash."""  
  response = send_to_bitly(
    url="http://api.bitly.com/v3/clicks_by_day",
    hashes=hashes,
    days=days,
  )
  if response: 
    for item in response['data']['clicks_by_day']:
      yield item

def send_to_bitly(url, hashes, **kwargs):
  params = [
    ('login', API_USER),
    ('apiKey', API_KEY),
  ]
  if not hashes: return
  for h in hashes:
    params.append(('hash', h))
  for key in kwargs:
    params.append((key, kwargs[key]))
  query = urllib.urlencode(params)
  fh = urllib.urlopen("%s?%s" % (url, query))
  content = fh.read()
  return json.loads(content)

class TestDomain(unittest.TestCase):
  def testInfo(self):
    """Input hashes should map to same hash."""
    input_hashes = ['qxzL1i', 'oWlf5E']
    output_hashes = [item['global_hash'] for item in info(input_hashes)]
    self.assertEquals(input_hashes, output_hashes)

if __name__ == '__main__':
  unittest.main()
