import sqlite3
from flask import jsonify
import datetime
import json
import os
import pandas as pd
import sqlalchemy
import uuid
SQLPATH = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'SQL'),'database.db')


class Sql():
    def __init__(self):
        self.initialize_db()
    def initialize_db(self):
        conn = sqlite3.connect(SQLPATH)
        
        c=conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS Json2Word ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT,email TEXT, Json TEXT)"
                )
        c.execute("CREATE TABLE IF NOT EXISTS API_KEYS ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, email TEXT, API_KEY TEXT)"
                )
        conn.commit()
        conn.close()
        
        
    def get_Json2Word(self, email):
        conn = sqlite3.connect("queries.db")
        c= conn.cursor()
        c.execute(f"SELECT * FROM Json2Word WHERE email = '{email}")
        data = c.fetchall()
        return data
    

    def insert_Json2Word(self, email,js):
        conn = sqlite3.connect(SQLPATH)
        c = conn.cursor()
        date=datetime.datetime.now()
        c.execute(f"""
                  INSERT INTO Json2Word (date,email, Json) values
                  ('{date}', '{email}','{js}')
                  """)
        conn.commit()
        c.close()


    def remove_data_with_id(self, id_to_remove):
        conn = sqlite3.connect(SQLPATH)
        c = conn.cursor()
        c.execute(f"DELETE FROM Json2Word WHERE id = {id_to_remove}")
        conn.commit()
        conn.close()
    

    def add_API_KEY(self, email):
        api_key = uuid.uuid4().hex
        conn = sqlite3.connect(SQLPATH)
        c = conn.cursor()
        c.execute(f"""
                  INSERT INTO api_keys (date,email, API_KEY) values
                  ('{datetime.datetime.now()}', '{email}','{api_key}')
                  """)
        
        conn.commit()
        conn.close()
    

    def API_KEY_match(self, API_KEY):
        conn = sqlite3.connect(SQLPATH)
        c= conn.cursor()
        c.execute(f"SELECT API_KEY FROM API_KEYS WHERE API_KEY = '{API_KEY}'")
        return any(c.fetchall()) # Returns True if c.fetchall contains any information.


    def get_all_API_KEYS(self):
        conn = sqlite3.connect(SQLPATH)
        c= conn.cursor()
        c.execute(f"SELECT API_KEY FROM API_KEYS")
        return [d[0] for d in c.fetchall()] # Returns True if c.fetchall contains any information.
    
            
    def get_Json2Word(self, email):
        conn = sqlite3.connect(SQLPATH)
        c= conn.cursor()
        c.execute(f"SELECT * FROM API_KEYS WHERE email = '{email}'")
        data = [d[0] for d in c.fetchall()]
        return data
    

    def __repr__(self):
        conn = sqlite3.connect(SQLPATH)
        
        return str(pd.read_sql('SELECT * FROM Json2Word', con=conn))


if __name__=='__main__':
    sql = Sql()
    sql.insert_Json2Word('amanda@löfkvist.eu',json.dumps({"Gnu":"Häst"}))
    sql.insert_Json2Word('Nisse@löfkvist.eu',json.dumps({"sa":"Häst"}))
    print(sql)
    sql.add_API_KEY("andreas.lofkvist@greenlandscaping.se")
    print(sql.get_all_API_KEYS())
    print(sql.API_KEY_match('40cc355a3efb4c98a27cbs68daa6841c8'))
    import logging
    from logging import log
    from logging.handlers import RotatingFileHandler
    log_filename = os.path.join(os.path.dirname(__file__),'flask_app.log')
    log_handler = RotatingFileHandler(log_filename, maxBytes=100000, backupCount=1)
    log_handler.setLevel(logging.INFO)
    log_filename = os.path.join(os.path.dirname(__file__),'error.log')
    log_handlers = RotatingFileHandler(log_filename, maxBytes=100000, backupCount=1)
    log_handlers.setLevel(logging.ERROR)
    log(logging.ERROR,"Error message")
    log(logging.INFO,"Info Message")