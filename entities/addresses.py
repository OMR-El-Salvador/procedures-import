import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Addresses(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'api.addresses'
    self._institution_code = institution_code
  
  def prepare(self): return #self._db.empty_table(self._table_name)
  
  def cleanup(self): self._db.complete_operations()

  def extract_str(self, collection, key):
    val = collection[key].strip()
    return None if val == '' else val

  def execute(self):
    self.prepare()

    with open('data/'+self._institution_code+'/addresses.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        detail = self.extract_str(row, 'detail')
        municipality = self.extract_str(row, 'municipality')
        mode_code = row['mode_code'].replace(' ', '')
        schedule = self.extract_str(row, 'schedule')
        phone = self.extract_str(row, 'phone')
        responsible_name = self.extract_str(row, 'responsible_name')
        responsible_position = self.extract_str(row, 'responsible_position')
        email = self.extract_str(row, 'email')

        qs = 'INSERT INTO ' + self._table_name
        qs += '(detail, municipality_id, mode_id, schedule, phone, responsible_name, '
        qs += 'responsible_position, email) '
        qs += 'VALUES (%s, %s, (SELECT id FROM api.modes WHERE code=%s), %s, %s, %s, '
        qs += '%s, %s);'
        values = (detail, municipality, mode_code, schedule, phone, responsible_name,
            responsible_position, email)
        self._db.create_record(qs, values)

    self.cleanup()
