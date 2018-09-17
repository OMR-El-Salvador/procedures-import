#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

options = {1: 'Procedures'}

print('Welcome to the OMR procedure import process!')
print('Current options:')

for key, value in options.items():
  print('%d) %s' % (key, value))

selected_option = int(input('Please enter your selection:'))

if selected_option in options:
  if selected_option == 1:
    with open('procedures.csv', encoding='iso-8859-1') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        code = row['code'].replace(' ', '')
        print(code)
else:
  input('Option not implemented, bye.')
  exit()
