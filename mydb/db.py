import psycopg2
from psycopg2 import sql
from configparser import ConfigParser

class Database:
    def __init__(self):
        self.connection = None
        self.load_config()
        
    def load_config(self):
        config = ConfigParser()
        config.read('config.ini')
        self.host = config.get('postgresql', 'host')
        self.user = config.get('postgresql', 'user')
        self.password = config.get('postgresql', 'password')
        self.database = config.get('postgresql', 'database')
        self.port = config.get('postgresql', 'port')

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.connection.autocommit = True
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            
    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def create_tables(self, plant):
        command = f"""
        CREATE TABLE IF NOT EXISTS ubot_{plant} (
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
            cursor = self.connection.cursor()
            cursor.execute(command)
            cursor.close()
            self.connection.commit()
            print('Table created successfully')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def select_data(self, table, bot_start=None, bot_end=None, plant=None, material=None, batch=None, inslot=None):
        cursor = self.connection.cursor()
        query = sql.SQL(f'SELECT * FROM {table} WHERE bot_start=%s AND bot_end=%s AND plant=%s AND material=%s AND batch=%s AND inslot=%s')
        cursor.execute(query, (bot_start, bot_end, plant, material, batch, inslot))

        rows = cursor.fetchall()
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
            
    def count_inslot(self, table):
        query = f"SELECT COUNT(*) FROM {table} WHERE inslot = TRUE;"
        return self.execute_query(query)[0][0]
    
    def count_botstart(self, table):
        query = f"SELECT COUNT(*) FROM {table} WHERE bot_start IS NOT NULL;"
        return self.execute_query(query)[0][0]