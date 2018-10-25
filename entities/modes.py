import csv
from .db import DB
from .abstract_entity import AbstractEntity

class Modes(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'api.modes'
    self._institution_code = institution_code

  def extract_val(self, collection, value):
    return None if value == '' or value=='0' else collection[int(value)]

  def extract_places(self, places):
    if places=='0' or places=='': return None
    payment_places = { 1: 'central_offices', 2: 'regional_offices', 3: 'financial_institution',
        4: 'online', 5: 'other', 6: 'treasury' }
    places_vals = places.replace(' ', '').split(',')
    result = []
    for place in places_vals: result.append(payment_places[int(place)])
    return result

  def extract_str(self, collection, key):
    val = collection[key].strip()
    return None if val == '' else val

  def prepare(self): return #self._db.empty_table(self._table_name)
  
  def cleanup(self): self._db.complete_operations()

  def execute(self):
    self.prepare()

    presentation_means = { 1: 'face', 2: 'face_online', 3: 'online' }
    validity_time_units = { 0: None, 1: 'day', 2: 'month', 3: 'year' }
    response_time_units = { 1: 'minute', 2: 'day' }
    legal_time_units = { 1: 'minute', 2: 'day', 3: 'month', 4: 'year' }
    classes_code = { 1: 'EMP', 2: 'CIU', 3: 'ORG', 4: 'OTR' }
    currencies = { 0: None, 1: 'dollar', 2: 'colon' }

    with open('data/'+self._institution_code+'/modes.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        procedure_code = row['procedure_code'].replace(' ', '')
        code = row['code'].replace(' ', '')
        name = 'Modalidad única' if code.endswith('0') else row['name'].strip()
        desc = self.extract_str(row, 'description')
        subject = self.extract_str(row, 'subject')
        presentation_mean = self.extract_val(presentation_means, row['presentation_mean'])
        presentation_url = self.extract_str(row, 'presentation_url')
        validity_time_unit = self.extract_val(validity_time_units, row['validity_time_unit'])
        validity_time_amt = self.extract_str(row, 'validity_time_amount')
        response_time_unit = self.extract_val(response_time_units, row['response_time_unit'])
        response_time_amt = self.extract_str(row, 'response_time_amount')
        legal_time_unit = self.extract_val(legal_time_units, row['legal_time_unit'])
        legal_time_amount = self.extract_str(row, 'legal_time_amount')
        responsible_area = self.extract_str(row, 'responsible_area')
        responsible_unit = self.extract_str(row, 'responsible_unit')
        class_code = self.extract_val(classes_code, row['class_code'])
        currency = self.extract_val(currencies, row['currency'])
        #TODO: Improve charge type handling
        charge_amount = None if row['charge_amount'].upper().replace(' ', '')=='P' \
            else row['charge_amount'].replace('$', '').replace(' ', '')
        charge_link = self.extract_str(row, 'charge_link')
        payment_places = self.extract_places(str(row['payment_places']))

        qs = 'INSERT INTO ' + self._table_name
        qs += '(code, name, description, procedure_id, subject, presentation_means, '
        qs += 'validity_time_unit, validity_time_amount, response_time_unit, response_time_amount, '
        qs += 'legal_time_unit, legal_time_amount, responsible_area, responsible_unit, class_id, '
        qs += 'currency, charge_amount, charge_link, payment_places, presentation_url) '
        qs += 'VALUES (%s, %s, %s, (SELECT id FROM api.procedures WHERE code=%s LIMIT 1), %s, %s, '
        qs += '%s, %s, %s, %s, '
        qs += '%s, %s, %s, %s, (SELECT id FROM api.classes WHERE code=%s LIMIT 1), '
        qs += '%s, %s, %s, %s::catalogs.places[], %s);'
        values = (code, name, desc, procedure_code, subject, presentation_mean,
            validity_time_unit, validity_time_amt, response_time_unit, response_time_amt,
            legal_time_unit, legal_time_amount, responsible_area, responsible_unit, class_code,
            currency, charge_amount, charge_link, payment_places, presentation_url)

        self._db.create_record(qs, values)

    self.cleanup()
