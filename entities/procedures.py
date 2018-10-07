import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Procedures(AbstractEntity):

  def __init__(self):
    self._db = DB()
    self._table_name = 'api.procedures'
  
  def prepare(self):
    self._db.empty_table(self._table_name)
  
  def cleanup(self):
    self._db.complete_operations()

  def execute(self):
    self.prepare()

    with open('data/procedures.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        code = row['code'].replace(' ', '')
        name = row['name']
        qs = 'INSERT INTO ' + self._table_name + ' (code, name) VALUES (%s, %s)'
        values = (code, name)
        self._db.create_record(qs, values)

    self.cleanup()
