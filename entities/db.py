import psycopg2

class DB():
  conn = None
  qty = 0

  def __init__(self):
    self.conn = psycopg2.connect(
      dbname='procedures_registry',
      user='postgres',
      password='p0stgr3$p0stgr3$',
      host='localhost')

  def create_record(self, qs, values):
    cur = self.conn.cursor()
    # print(cur.mogrify(qs,values))
    cur.execute(qs, values)
    self.qty += 1

  def empty_table(self, table):
    cur = self.conn.cursor()
    cur.execute('DELETE FROM ' + table + ';')

  def complete_operations(self):
    print(str(self.qty) + ' rows affected.')
    self.conn.commit()
    self.conn.close()
