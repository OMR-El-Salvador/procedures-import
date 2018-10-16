import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Addresses(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'public.addresses'
    self._institution_code = institution_code
  
  def prepare(self):
    return #self._db.empty_table(self._table_name)
  
  def cleanup(self):
    self._db.complete_operations()

  def execute(self):
    self.prepare()

    with open('data/'+self._institution_code+'/addresses.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        detail = row['detail']
        municipality = row['municipality'].rstrip()
        mode_code = row['mode_code'].replace(' ', '')
        schedule = row['schedule']
        phone = row['phone']
        responsible_name = row['responsible_name']
        responsible_position = row['responsible_position']
        email = row['email']

        qs = 'INSERT INTO ' + self._table_name
        qs += '(detail, municipality_id, mode_id, schedule, phone, responsible_name, '
        qs += 'responsible_position, email) '
        qs += 'VALUES (%s, %s, (SELECT id FROM api.modes WHERE code=%s), %s, %s, %s, '
        qs += '%s, %s);'
        values = (detail, municipality, mode_code, schedule, phone, responsible_name,
            responsible_position, email)
        self._db.create_record(qs, values)

    self.cleanup()
