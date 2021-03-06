import csv
from .db import DB
from .abstract_entity import AbstractEntity

class LegalBase(AbstractEntity):

  def __init__(self, institution_code):
    self._db = DB()
    self._table_name = 'api.legal_base'
    self._institution_code = institution_code
  
  def prepare(self): return #self._db.empty_table(self._table_name)
  
  def cleanup(self): self._db.complete_operations()

  def extract_str(self, collection, key):
    val = collection[key].strip()
    return None if (val == '' or val == '0') else val

  def execute(self):
    self.prepare()

    legis_type = { 'Ley': 'law', 'Reglamento de Ley': 'regulation', 'No Existe': 'non_existent',
        'Acuerdo Ministerial': 'ministerial_agreement', 'Otro': 'other',
        'Constitución': 'constitution', 'Tratado Internacional': 'international_treaty',
        'Reglamento Técnico': 'technical_regulation', 'Decreto Ejecutivo': 'executive_order',
        'Reglamento': 'regulation', 'Tratado': 'international_treaty', 'No existe': 'non_existent',
        'Reglamento de ley': 'regulation', 'Reglamento Tecnico': 'technical_regulation',
        'otro': 'other' }

    with open('data/'+self._institution_code+'/legal_base.csv', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        #If not applicable there should not be a record
        if row['legislation_type'].upper()=='NO APLICA': continue

        mode_code = row['mode_code'].replace(' ', '')
        base_type = legis_type[row['legislation_type'].strip()]
        name = self.extract_str(row, 'legislation_name')
        reference = self.extract_str(row, 'legislation_name')
        topic = self.extract_str(row, 'legal_topic')

        qs = 'INSERT INTO ' + self._table_name
        qs += '(mode_id, type, legislation_name, legislation_reference, '
        qs += 'legal_topic_id)'
        qs += 'VALUES ((SELECT id FROM api.modes WHERE code=%s), %s, %s, %s, '
        qs += '(SELECT id FROM api.legal_topics WHERE UPPER(name)=UPPER(%s)))'
        values = (mode_code, base_type, name, reference,
            topic)
        self._db.create_record(qs, values)

    self.cleanup()
