import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Forms(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'public.forms'
    self._institution_code = institution_code
  
  def prepare(self): return #self._db.empty_table(self._table_name)
  
  def cleanup(self): self._db.complete_operations()

  def extract_str(self, collection, key):
    val = collection[key].strip()
    return None if val == '' else val

  def execute(self):
    self.prepare()

    with open('data/'+self._institution_code+'/forms.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if row['solicited']=='': continue

        mode_code = row['mode_code'].replace(' ', '')
        name = self.extract_str(row, 'name')

        url = None
        file = None
        val = self.extract_str(row, 'url')

        if 'http' in val: url = val
        else: file = val

        qs = 'INSERT INTO ' + self._table_name
        qs += '(mode_id, name, url) '
        qs += 'VALUES ((SELECT id FROM api.modes WHERE code=%s), %s, %s, %s);'
        values = (mode_code, name, url, file)
        self._db.create_record(qs, values)

    self.cleanup()
