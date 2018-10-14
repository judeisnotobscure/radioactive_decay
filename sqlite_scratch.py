#!/usr/bin/env python3
import sqlite3

class Sql:
    def __init__(self, database):
        try: 
            if ".db" or ".sql" in database:
                self.database = database
            else:
                print("Sql instance not created:\nPlease use a valid database filename")
        except Exception as e:
            print("Error:", e)

    def create_conn(self):
        purpose = """ Creates a database connection to this.database file.
    Usage: createConn()
    """
        try:
            self.conn = sqlite3.connect(self.database)
            return self.conn
        except Exception as e:
            print(purpose, "\nError:", e)
    
    def write_table(self, sql_statement):
        purpose = """ Writes new tables or data to the self.database
        Usage: write_table(sql_statement)
        Args: 
        sql_statement = sql commands ie.. CREATE IF NOT EXISTS table_name(row_info)
        """
        try: 
            c = self.conn.cursor()
            c.execute(sql_statement)
        except Exception as e:
            print(purpose, "\nError:",e)

    def read_table(self, sql_statement):
        purpose = """ Reads data from self.database
        Usage: read_table(sql_statement)
        Args:
        sql_statement = sql commands ie.. SELECT * FROM table_name
        """
        try: 
            c = self.conn.cursor()
            c.execute(sql_statement)
            rows = c.fetchall()
        except Exception as e:
            print(purpose,"\nError:",e)
        for row in rows:
            print(row)

    def close_conn(self):
        self.conn.commit()
        self.conn.close()