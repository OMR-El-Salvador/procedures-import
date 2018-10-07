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

    with open('data/modes.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        procedure_code = row['procedure_code'].replace(' ', '')
        code = row['code'].replace(' ', '')
        name = 'Modalidad única' if code.endswith('0') else row['name']
        desc = row['description']

        qs = 'INSERT INTO ' + self._table_name + '(code, name, description, procedure_id)'
        qs += 'VALUES (%s, %s, %s, (SELECT id FROM api.procedures WHERE code = %s LIMIT 1))'
        values = (code, name, desc, procedure_code)
        self._db.create_record(qs, values)

    self.cleanup()
