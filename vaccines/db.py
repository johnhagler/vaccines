import sqlite3


class SQLite3(object):

    @staticmethod
    def insert(cursor, table='', rows=[]):
        sql = 'insert into %s values( %s )' % (table, ('?,' * len(rows))[:-1])
        cursor.execute(sql, rows)

    @staticmethod
    def insertmany(cursor, table='', rows=[]):
        if len(rows) > 0:
            sql = 'insert into %s values( %s )' % (table, ('?,' * len(rows[0]))[:-1])
            cursor.executemany(sql, rows)

    def __init__(self, file_name, schema_file=''):
        print 'Connecting to %s' % file_name
        self.conn = sqlite3.connect(file_name)

        self.conn.text_factory = str
        self.conn.row_factory = sqlite3.Row

        if schema_file:
            print 'Generating db schema form %s' % schema_file
            with open(schema_file, mode='r') as f:
                contents = f.read()
                scripts = contents.split(';')
                for script in scripts:
                    script.strip()
                    if script:
                        self.conn.cursor().execute(script)

                self.conn.commit()

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.conn.close()
