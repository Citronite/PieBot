import sqlite3

class Sqlite(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
      	super().__init__(*args, **kwargs)
      	self.cursor = self.cursor()
      	self.row_factory = sqlite3.Row

    def c_exec(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)

    def c_execmany(self, *args, **kwargs):
        return self.cursor.executemany(*args, **kwargs)

    def c_execscript(self, *args, **kwargs):
        return self.cursor.executescript(*args, **kwargs)

    def finish(self):
      	self.commit()
      	self.cursor.close()
      	self.close()

    def fetch(self, size = 1):
      	if size <= 0:
          	return self.cursor.fetchall()
      	elif size == 1:
          	return self.cursor.fetchone()
      	else:
          	return self.cursor.fetchmany(size)

    def select(self, query, size = 1):
        self.c_exec(query)
        return self.fetch(size)
    def selectmany(self, *args, **kwargs):
        self.c_execmany(*args, **kwargs)
        return self.fetch(0)
