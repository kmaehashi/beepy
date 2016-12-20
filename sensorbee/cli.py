# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import json
import optparse

from .api import SensorBeeAPI
from .tools.spider import Spider
from .tools.dot import DotView
from .tools.top import TopView

class _OptionParser(optparse.OptionParser, object):
    def __init__(self, *args, **kwargs):
        self._error = False
        super(_OptionParser, self).__init__(*args, **kwargs)

    def error(self, msg):
        self._msg = msg
        self._error = True

def print_out(out, msg):
    out.write(msg)

class SbStatCommand(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self._out = out
        self._err = err
        self._parser = self._create_parser()

    def main(self, argv):
        err = self._err
        (params, _) = self._parser.parse_args(argv + [''])  # [''] is added to workaround optparse bug

        # Failed to parse options.
        if self._parser._error:
            print_out(err, 'Error: {0}'.format(self._parser._msg))
            self.print_usage()
            return 2

        # Help option is specified.
        if params.help:
            self.print_usage()
            return 0

        # Validate parameters.
        if params.port < 1 or 65535 < params.port:
            print_out(err, 'Error: port number out of range: {0}\n'.format(params.port))
            self.print_usage()
            return 1
        if params.json and params.topology:
            print_out(err, 'Error: --json and --topology cannot be used at once\n')
            self.print_usage()
            return 1
        if params.json and params.dot:
            print_out(err, 'Error: --json and --dot cannot be used at once\n')
            self.print_usage()
            return 1

        api = SensorBeeAPI(params.host, params.port)

        if params.json:
            # Raw JSON mode
            json.dump(Spider(api).get(), self._out, indent=4)
            print_out(self._out, '\n')
            return 0

        # Determine which topology to use.
        topos = [t['name'] for t in api.topologies()['topologies']]
        if params.topology is None:
            if len(topos) == 1:
                print_out(err, 'Using topology: {0}\n'.format(topos[0]))
                params.topology = topos[0]
            else:
                print_out(err, 'Error: --topology must be specified when multiple topologies are available\n')
                print_out(err, 'Topologies: {0}\n'.format(', '.join(topos)))
                return 1
        else:
            if params.topology not in topos:
                print_out(err, 'Error: topology {0} not found\n'.format(params.topology))
                print_out(err, 'Topologies: {0}\n'.format(', '.join(sorted(topos))))
                return 1

        if params.dot:
            # DOT mode
            print_out(self._out, DotView(api).render(params.topology))
            print_out(self._out, '\n')
        else:
            # Top mode (default)
            print_out(self._out, TopView(api).render(params.topology))
            print_out(self._out, '\n')

        return 0

    def _create_parser(self):
        parser = _OptionParser(add_help_option=False)
        parser.add_option('-H', '--host', type='string', default='127.0.0.1',
                          help='host name or IP address of the server (default: %default)')
        parser.add_option('-P', '--port', type='int', default=15601,
                          help='port number of the server (default: %default)')
        parser.add_option('-t', '--topology', type='string', default=None,
                          help='topology name (first one is used if not given)')
        parser.add_option('--json', default=False, action='store_true',
                          help='dump results as JSON')
        parser.add_option('--dot', default=False, action='store_true',
                          help='dump results as DOT')
        parser.add_option('--help', default=False, action='store_true',
                          help='print the usage and exit')
        return parser

    def print_usage(self):
        err = self._err
        print_out(err, '\n')
        print_out(err, 'sbstat - SensorBee Status Monitoring Tool\n')
        print_out(err, '\n')
        self._parser.print_help(err)
        print_out(err, '\n')

def sbstat():
    cmd = SbStatCommand()
    retval = cmd.main(sys.argv)
    sys.exit(retval)