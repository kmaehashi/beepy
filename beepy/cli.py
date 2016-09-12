#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import json

from .tools import BeePyDump

def _beepy():
  args = sys.argv[1:]
  host = args[0] if len(args) > 0 else '127.0.0.1'
  port = args[1] if len(args) > 1 else '15601'
  print(json.dumps(BeePyDump(host, port).dump(), indent=4))

def _beepy_dot():
  args = sys.argv[1:]
  host = args[0] if len(args) > 0 else '127.0.0.1'
  port = args[1] if len(args) > 1 else '15601'
  topo = args[2] if len(args) > 2 else 'main'
  print(BeePyDump(host, port).dump_dot_for(topo))
