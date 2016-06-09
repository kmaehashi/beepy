# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import json

try:
  from urllib.request import urlopen
except ImportError:
  from urllib2 import urlopen

class BeePyAPI(object):
  def __init__(self, host='127.0.0.1', port=15601):
    self.host = host
    self.port = port

  def _req(self, path):
    url = 'http://{0}:{1}/api/v1/{2}'.format(self.host, self.port, path)
    return json.loads(urlopen(url).read().decode())

  def runtime_status(self):
    return self._req('runtime_status')

  def topologies(self):
    return self._req('topologies')

  def topology(self, t):
    return self._req('topologies/{0}'.format(t))

  def sources(self, t):
    return self._req('topologies/{0}/sources'.format(t))

  def source(self, t, s):
    return self._req('topologies/{0}/sources/{1}'.format(t, s))

  def streams(self, t):
    return self._req('topologies/{0}/streams'.format(t))

  def stream(self, t, s):
    return self._req('topologies/{0}/streams/{1}'.format(t, s))

  def sinks(self, t):
    return self._req('topologies/{0}/sinks'.format(t))

  def sink(self, t, s):
    return self._req('topologies/{0}/sinks/{1}'.format(t, s))
