#!/usr/bin/env python3
# -*- coding: utf-8 -*-

options = {1: 'Procedures'}

print('Welcome to the OMR procedure import process!')
print('Current options:')

for key, value in options.items():
  print('%d) %s' % (key, value))

selected_option = int(input('Please enter your selection:'))

if selected_option in options:
  entities = None

  if selected_option == 1:
    from entities.procedures import Procedure
    entities = Procedure()

  entities.execute()
else:
  print('Option not implemented, bye.')
  exit()
