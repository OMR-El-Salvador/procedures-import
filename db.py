import psycopg2

conn = psycopg2.connect(
  dbname='procedures_registry',
  user='postgres',
  password='p0stgr3$p0stgr3$',
  host='localhost')

def create_record(qs, values):
  cur = conn.cursor()
  cur.execute(qs, values)

def complete_operations():
  conn.commit()
  conn.close()
