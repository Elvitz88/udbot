import psycopg2
from psycopg2 import sql
from configparser import ConfigParser

class Database:

    def __init__(self):
        self.conn = None

    @staticmethod
    def config(filename='config.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            # create a cursor
            cur = self.conn.cursor()
            
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            # cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # finally:
        #     if self.conn is not None:
        #         self.conn.close()
        #         print('Database connection closed.')

    def create_tables(self,plant):
        command = f"""
        CREATE TABLE ubot_{plant} (
            bot_start TIMESTAMP,
            bot_end TIMESTAMP,
            plant VARCHAR(255),
            material VARCHAR(255),
            batch VARCHAR(255),
            inslot VARCHAR(255),
            udcode VARCHAR(255)
        )
        """

        try:
            cur = self.conn.cursor()
            cur.execute(command)
            cur.close()
            self.conn.commit()
            print('Table created successfully')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def select_data(self, table, bot_start=None, bot_end=None, plant=None, material=None, batch=None, inslot=None):
        cur = self.conn.cursor()
        query = sql.SQL(f'SELECT * FROM {table} WHERE bot_start=%s AND bot_end=%s AND plant=%s AND material=%s AND batch=%s AND inslot=%s')
        cur.execute(query, (bot_start, bot_end, plant, material, batch, inslot))

        rows = cur.fetchall()
        for row in rows:
            print(row)

    def update_data(self, table, set_column, set_value, where_column, where_value):
        cur = self.conn.cursor()
        query = sql.SQL(f'UPDATE {table} SET {set_column}=%s WHERE {where_column}=%s')
        cur.execute(query, (set_value, where_value))

        self.conn.commit()

    def insert_data(self, table, columns, values):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {} ({}) VALUES (%s, %s, %s, %s, %s, %s, %s)").format(
            sql.Identifier(table), 
            sql.SQL(",").join(map(sql.Identifier, columns.split(", "))))
        cur.execute(query, values)
        self.conn.commit()

    def truncate_table(self, table):
        cur = self.conn.cursor()
        query = sql.SQL(f'TRUNCATE {table}')
        cur.execute(query)

        self.conn.commit()

    def close_conn(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')