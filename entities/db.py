import psycopg2

class DB():
  conn = None

  def __init__(self):
    self.conn = psycopg2.connect(
      dbname='procedures_registry',
      user='postgres',
      password='p0stgr3$p0stgr3$',
      host='localhost')

  def create_record(self, qs, values):
    cur = self.conn.cursor()
    cur.execute(qs, values)

  def empty_table(self, table):
    cur = self.conn.cursor()
    cur.execute('DELETE FROM ' + table + ';')

  def complete_operations(self):
    self.conn.commit()
    self.conn.close()
