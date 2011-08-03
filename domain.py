#!/usr/bin/env python
from urlparse import urlparse
import re
import unittest

DOMAIN_RE = re.compile('([^.]+\.[^.]+)$')

def domain(url):
  """Returns the two-level domain part of a URL."""
  netloc = urlparse(url)[1]
  match = DOMAIN_RE.search(netloc)
  if match:
    return match.groups()[0]

class TestDomain(unittest.TestCase):
  def testDomain(self):
    self.assertEquals(domain("http://spam.eggs"), "spam.eggs")
    self.assertEquals(domain("http://foo.bar.baz"), "bar.baz")

if __name__ == '__main__':
  unittest.main()
