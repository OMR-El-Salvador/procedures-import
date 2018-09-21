import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Modes(AbstractEntity):

  def __init__(self):
    self._db = DB()
    self._table_name = 'api.modes'
  
  def prepare(self):
    self._db.empty_table(self._table_name)
  
  def cleanup(self):
    self._db.complete_operations()

  def execute(self):
    self.prepare()

    with open('data/modes.csv', encoding='iso-8859-1') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        procedure_code = row['procedure_code'].replace(' ', '')
        code = row['code'].replace(' ', '')
        name = row['name'].split('-')[1]
        # qs = 'INSERT INTO ' + self._table_name + ' (code, name, description) VALUES (%s, %s, %s)'
        # values = (code, name, desc)
        # self._db.create_record(qs, values)
        print('Imported: ' + procedure_code + ' ' + code + ' ' + name)

    self.cleanup()
