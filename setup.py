

from mydb.db import Database
#
db = Database()
db.connect()
plants = ['A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'A007', 'A008', 'A009', 'A011']

for plant in plants:
    db.create_tables(plant)
db.close_conn()