# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib
import json
import email.parser

try:
  from urllib.request import urlopen, Request
except ImportError:
  from urllib2 import urlopen, Request

class BeePyAPI(object):
  def __init__(self, host='127.0.0.1', port=15601):
    self.host = host
    self.port = port

  def _url(self, path, scheme='http'):
    return '{0}://{1}:{2}/api/v1/{3}'.format(scheme, self.host, self.port, path)

  def _req(self, path, data=None, method=None):
    if method is None:
      method = 'GET' if data is None else 'POST'
    req = Request(self._url(path), data=data)
    req.get_method = lambda: method
    return json.loads(urlopen(req).read().decode())

  def runtime_status(self):
    return self._req('runtime_status')

  def topologies(self):
    return self._req('topologies')

  def topology(self, t):
    return self._req('topologies/{0}'.format(t))

  def create_topology(self, t):
    return self._req('topologies', json.dumps({'name': t}).encode())

  def delete_topology(self, t):
    return self._req('topologies/{0}'.format(t), None, 'DELETE')

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

  def query(self, t, q):
    close = True
    f = urlopen(self._url('topologies/{0}/queries'.format(t)), json.dumps({'queries': q}).encode())
    try:
      msg = _MessageWrapper(f.info())
      mimetype = msg.get_content_type()
      if mimetype == 'application/json':
        return json.loads(f.read().decode())
      elif mimetype == 'multipart/mixed':
        rs = ResultSet(f, msg.get_param('boundary'))
        close = False
        return rs
      else:
        raise RuntimeError('unexpected MIME type: {0}'.format(mimetype))
    finally:
      if close:
        f.close()

class _MessageWrapper(object):
  def __init__(self, msg):
    self.msg = msg

  def get_content_type(self, *args, **kwargs):
    if hasattr(self.msg, 'gettype'):
      return self.msg.gettype(*args, **kwargs)
    return self.msg.get_content_type(*args, **kwargs)

  def get_param(self, *args, **kwargs):
    if hasattr(self.msg, 'getparam'):
      return self.msg.getparam(*args, **kwargs)
    return self.msg.get_param(*args, **kwargs)

class ResultSet(object):
  def __init__(self, _f, _boundary):
    self._f = _f
    self._boundary = _boundary

  def __del__(self):
    f = self._f
    if f:
      f.close()

  def __iter__(self):
    with contextlib.closing(self._f) as f:
      parser = email.parser.FeedParser()
      while True:
        line = f.readline()
        if not line: break
        if line.rstrip() == '--{0}'.format(self._boundary).encode():
          line = f.readline()
          while line.rstrip():
            parser.feed(line.decode())
            line = f.readline()
          yield json.loads(f.read(int(parser.close()['Content-Length'])).decode())
          parser = email.parser.FeedParser()
