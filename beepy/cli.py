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

def _beetop():
  args = sys.argv[1:]
  host = args[0] if len(args) > 0 else '127.0.0.1'
  port = args[1] if len(args) > 1 else '15601'
  topo = args[2] if len(args) > 2 else 'main'
  dump = BeePyDump(host, port).dump()


  # TODO refactor the following code...
  td = dump['topologies'][topo]

  def fmt_queue(num, size):
    ratio = num / size * 100 if size != 0 else 0
    return '{0} ({1:3.1f}%)'.format(num, ratio)

  def sorted_keys(td):
    sources = sorted(td['sources'].keys())
    outputs = []
    for source_outputs in sorted([x['status']['output_stats']['outputs'].keys() for x in td['sources'].values()]):
      for source_output in sorted(source_outputs):
        if source_output not in outputs:
          outputs.append(source_output)
    while True:
      found_outputs = []
      for out in sorted(filter(lambda x: x in td['streams'], outputs)):
        for found_out in sorted(td['streams'][out]['status']['output_stats'].keys()):
          if found_out not in found_outputs and found_out not in outputs:
            found_outputs.append(found_out)
      if len(found_outputs) == 0:
        break
      outputs += found_outputs

    streams = filter(lambda x: x in td['streams'], outputs)
    dangling_streams = filter(lambda x: x not in outputs, sorted(td['streams'].keys()))
    sinks = filter(lambda x: x in td['sinks'], outputs)
    dangling_sinks = filter(lambda x: x not in outputs, sorted(td['sinks'].keys()))

    return (sources, streams + dangling_streams, sinks + dangling_sinks)

  (sources, streams, sinks) = sorted_keys(td)

  lines = [
    ['Node', 'Status', 'Received', 'Error', 'Output', '(sent)', '(queued)', '(dropped)']
  ]

  for name in sources:
    stat = td['sources'][name]
    output_stat = stat['status']['output_stats']
    (queue_count_total, queue_size_total) = (0, 0)
    v_outs = []
    for (k, v) in output_stat['outputs'].items():
      queue_count_total += v['num_queued']
      queue_size_total += v['queue_size']
      v_outs.append(['', '', '', '', '  ' + k, v['num_sent'], fmt_queue(v['num_queued'], v['queue_size']), ''])
    lines.append(['> ' + stat['name'], stat['state'], '', '', '(total)', output_stat['num_sent_total'], fmt_queue(queue_count_total, queue_size_total), output_stat['num_dropped']])
    lines += v_outs

  for name in streams:
    stat = td['streams'][name]
    input_stat = stat['status']['input_stats']
    output_stat = stat['status']['output_stats']
    (queue_count_total, queue_size_total) = (0, 0)
    v_outs = []
    for (k, v) in output_stat['outputs'].items():
      queue_count_total += v['num_queued']
      queue_size_total += v['queue_size']
      v_outs.append(['', '', '', '', '  ' + k, v['num_sent'], fmt_queue(v['num_queued'], v['queue_size']), ''])
    lines.append(['| ' + stat['name'], stat['state'], input_stat['num_received_total'], input_stat['num_errors'], '(total)', output_stat['num_sent_total'], fmt_queue(queue_count_total, queue_size_total), output_stat['num_dropped']])
    lines += v_outs

  for name in sinks:
    stat = td['sinks'][name]
    input_stat = stat['status']['input_stats']
    lines.append(['< ' + stat['name'], stat['state'], input_stat['num_received_total'], input_stat['num_errors'], '', '', '', ''])

  col_lengths = [0] * 8
  for line in lines:
    for i in range(len(line)):
      col_lengths[i] = max(col_lengths[i], len(str(line[i])))

  fmt = '{:' + str(col_lengths[0] + 2) + '}' + ''.join(['{:' + str(x+2) + '}' for x in col_lengths[1:]])
  for line in lines:
    print(fmt.format(*map(str, line)))
