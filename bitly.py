#!/usr/bin/python

import httplib
import urllib
import json
import unittest

API_USER = 'gogogon'
API_KEY  = 'R_cbcba050cbd86f7b2fb2a6b3e34f7c4c'

def info(*hashes):
  """Yields info for each given hash."""
  params = [
    ('login', API_USER),
    ('apiKey', API_KEY),
  ]
  if not hashes: return
  for h in hashes:
    params.append(('hash', h))
  query = urllib.urlencode(params)
  url = "http://api.bitly.com/v3/info"
  fh = urllib.urlopen("%s?%s" % (url, query))
  content = fh.read()
  response = json.loads(content)
  for item in response['data']['info']:
    yield item

class TestDomain(unittest.TestCase):
  def testInfo(self):
    """Input hashes should map to same hash."""
    input_hashes = ['qxzL1i', 'oWlf5E']
    output_hashes = [item['global_hash'] for item in info(*input_hashes)]
    self.assertEquals(input_hashes, output_hashes)

if __name__ == '__main__':
  unittest.main()
