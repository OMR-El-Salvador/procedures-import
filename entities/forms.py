import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Forms(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'public.forms'
    self._institution_code = institution_code
  
  def prepare(self):
    self._db.empty_table(self._table_name)
  
  def cleanup(self):
    self._db.complete_operations()

  def execute(self):
    self.prepare()

    with open('data/'+self._institution_code+'/forms.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if row['solicited']=='': continue
        
        mode_code = row['mode_code'].replace(' ', '')
        name = row['name']
        url = row['url']

        qs = 'INSERT INTO ' + self._table_name
        qs += '(mode_id, name, url) '
        qs += 'VALUES ((SELECT id FROM api.modes WHERE code=%s), %s, %s);'
        values = (mode_code, name, url)
        self._db.create_record(qs, values)

    self.cleanup()
