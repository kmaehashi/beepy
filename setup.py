#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='beepy',
      version='0.0.1',
      author='Kenichi Maehashi',
      author_email='webmaster@kenichimaehashi.com',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      entry_points={
          'console_scripts': [
              'beepy=beepy.cli:_beepy',
              'beepy_dot=beepy.cli:_beepy_dot',
          ],
      },
      packages=['beepy'],
)
