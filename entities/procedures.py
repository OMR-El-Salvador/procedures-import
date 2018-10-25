import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Procedures(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'api.procedures'
    self._institution_code = institution_code
  
  def prepare(self): return #self._db.empty_table(self._table_name)

  def cleanup(self): self._db.complete_operations()

  def execute(self):
    self.prepare()

    with open('data/'+self._institution_code+'/procedures.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        code = row['code'].replace(' ', '')
        name = row['name'].strip()
        qs = 'INSERT INTO ' + self._table_name
        qs += '(code, name, institution_id) VALUES (%s, %s, '
        qs += '(SELECT id FROM api.institutions WHERE code=%s));'
        values = (code, name, self._institution_code)
        self._db.create_record(qs, values)

    self.cleanup()
