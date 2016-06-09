# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict

from .api import BeePyAPI

class BeePyDump(object):
  def __init__(self, host='127.0.0.1', port=15601):
    self._api = BeePyAPI(host, port)

  def dump_dot_for(self, t):
    buf = ['digraph {']

    for s in map(lambda x: x['name'], self._api.sources(t)['sources']):
      v = self._api.source(t, s)['source']['status']['output_stats']['outputs']
      for out in v.keys():
        buf += ['{0} -> {1}'.format(s, out)]

    for s in map(lambda x: x['name'], self._api.streams(t)['streams']):
      v = self._api.stream(t, s)['stream']['status']['output_stats']['outputs']
      for out in v.keys():
        buf += ['{0} -> {1}'.format(s, out)]

    buf += ['}']

    return '\n'.join(buf)

  def dump(self):
    server = defaultdict(dict)
    server['runtime_status'] = self._api.runtime_status()

    for t in map(lambda x: x['name'], self._api.topologies()['topologies']):
      topology = defaultdict(dict)
      for s in map(lambda x: x['name'], self._api.sources(t)['sources']):
        topology['sources'][s] = self._api.source(t, s)['source']
      for s in map(lambda x: x['name'], self._api.streams(t)['streams']):
        topology['streams'][s] = self._api.stream(t, s)['stream']
      for s in map(lambda x: x['name'], self._api.sinks(t)['sinks']):
        topology['sinks'][s] = self._api.sink(t, s)['sink']
      server['topologies'][t] = topology

    return server
