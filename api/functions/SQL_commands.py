import sqlite3
from flask import jsonify


class Sql():
    def initialize_db():
        c = sqlite3.connect("queries.db").cursor()
        c.execute("CREATE TABLE IF NOT EXISTS history ( \
                id text, address TEXT, query TEXT, status TEXT)"
                )
        c.connection.close()

    def get_queries():
        c = sqlite3.connect("queries.db").cursor()
        c.execute("SELECT * FROM history")
        data = c.fetchall()
        return jsonify(data)
    