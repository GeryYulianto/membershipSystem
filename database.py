import sqlite3
from flask import *

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        create_users_table()
        create_transaction_table()
        create_attendance_table()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv


#Migrations
def create_users_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        no_hp TEXT NOT NULL,
        type TEXT NOT NULL
    )
    '''
    query_db(create_table_query)

def create_attendance_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomor_kehadiran INTEGER NOT NULL,
        date_time DATETIME NOT NULL,
        FOREIGN KEY (id) REFERENCES users(id)
    )
    '''
    query_db(create_table_query)

def create_transaction_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS payment (
        id INTEGER,
        fee FLOAT NOT NULL,
        date_time DATETIME NOT NULL,
        FOREIGN KEY (id) REFERENCES users(id)
    )
    '''
    query_db(create_table_query)