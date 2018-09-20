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
  import db

  if selected_option == 1:
    with open('procedures.csv', encoding='iso-8859-1') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        code = row['code'].replace(' ', '')
        name = row['name']
        desc = row['description']
        qs = 'INSERT INTO api.procedures(code, name, description) VALUES (%s, %s, %s)'
        values = (code, name, desc)
        db.create_record(qs, values)
        print('Imported: ' + code)

  db.complete_operations()
else:
  print('Option not implemented, bye.')
  exit()
