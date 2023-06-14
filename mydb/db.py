import psycopg2
from psycopg2 import sql
from configparser import ConfigParser
import pandas as pd

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
            
    def execute_query(self, query, values=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            try:
                result = cursor.fetchall()
                return result
            except psycopg2.ProgrammingError:
                # For queries that don't return anything
                pass

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

    def get_data(self, plant, bot_start=None, bot_end=None):
        with self.connection.cursor() as cursor:
            # Define the query
            query = f"SELECT * FROM ubot_{plant}"
            
            # Add the conditions if they are specified
            if bot_start is not None and bot_end is not None:
                query += f" WHERE bot_start >= '{bot_start}' AND bot_end <= '{bot_end}'"

            cursor.execute(query)

            # Fetch all the data returned by the database
            rows = cursor.fetchall()
                
            # Create a dataframe from the rows
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

            return df
            
            
    def update_data(self, table, set_column, set_value, conditions):
        with self.connection.cursor() as cursor:
            condition_str = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
            query = sql.SQL(f'UPDATE {table} SET {set_column} = %s WHERE {condition_str}')
            cursor.execute(query, (set_value, *conditions.values()))
            self.connection.commit()

    def insert_data(self, table, columns, values):
        cursor = self.connection.cursor()
        query = sql.SQL("INSERT INTO {} ({}) VALUES (%s, %s, %s, %s, %s, %s, %s)").format(
            sql.Identifier(table), 
            sql.SQL(",").join(map(sql.Identifier, columns.split(", "))))
        cursor.execute(query, values)
        self.connection.commit()

    def truncate_table(self, table):
        cursor = self.connection.cursor()
        query = sql.SQL(f'TRUNCATE {table}')
        cursor.execute(query)

        self.connection.commit()

    def close_conn(self):
        if self.connection is not None:
            self.connection.close()
            print('Database connection closed.')