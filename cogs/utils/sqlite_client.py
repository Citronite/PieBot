import sqlite3

class Sqlite_client(sqlite3.Connection):
    """
    sqlite3 database client. Basically, provides 
    some shorthands for basic db functions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor = self.cursor()                     # Create a "default" cursor for the instance
        self.row_factory = sqlite3.Row                  # sqlite3.Row is supposed to be a "highly optimized row_factory for Connection objects"
        self.exec = self.cursor.execute                 # Shorthand for default cursor's execute function 
        self.execmany = self.cursor.executemany         # Shorthand for default cursor's executemany function
        self.execscript = self.cursor.executescript     # Shorthand for default cursor's executescript function
    
    def finish(self):
        self.commit()
        self.cursor.close()
        self.close()

    # Handy function for calling default cursor's fetch functions.
    def fetch(self, size: int):
        if size <= 0:
            return self.cursor.fetchall()
        elif size == 1:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchmany(size)



