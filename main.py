#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from entities import *

options = { 1: Procedures, 2: Modes }

print('Welcome to the OMR procedure import process!')
print('Current options:')

for key, value in options.items():
  print('%d) %s' % (key, value.__name__))

try:
  selected_option = int(input('Please enter your selection:'))
  instance = options[selected_option]()
  instance.execute()
except KeyError:
  print('Not implemented option.')
except Exception as ex:
  print('Error: ' + str(ex))

print('So long and thanks for all the fish!')
