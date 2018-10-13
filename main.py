#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from entities import *

options = { 1: Procedures, 2: Modes, 3: LegalBase, 4: Addresses, 5: Forms }

print('Welcome to the OMR procedure import process!')
print('Current options:')

for key, value in options.items():
  print('%d) %s' % (key, value.__name__))

selected_option = int(input('Please enter data to import:'))
institution_code = input('Please enter institution code:').upper()
instance = options[selected_option](institution_code)
instance.execute()

print('So long and thanks for all the fish!')
