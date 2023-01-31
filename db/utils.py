import sqlite3
import os

script_dir = os.path.abspath(os.path.dirname( __file__ ))
conn = sqlite3.connect(script_dir + '/../monkeybet.db')

def setup():
  cursor = conn.cursor()

  cursor.execute(
    'CREATE TABLE IF NOT EXISTS JOGOS ('+
    'id INTEGER PRIMARY KEY, '+
    'data TEXT, '+
    'horario TEXT, '+
    'descricao TEXT, '+
    'banca TEXT, '+
    'odd1 FLOAT, '+
    'oddx FLOAT, '+
    'odd2 FLOAT, '+
    'palpite TEXT, '+
    'dupla_hipotese TEXT)'
  )

def insert_row(data):
  cursor = conn.cursor()

  sql = """INSERT INTO JOGOS(id, data, horario, descricao, banca, odd1, oddx, odd2, palpite, dupla_hipotese)
    VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

  cursor.execute(sql, data)
  conn.commit()

def count_date(date):
  cursor = conn.cursor()

  sql = "SELECT COUNT(id) FROM JOGOS WHERE data=?"

  cursor.execute(sql, [date])

  return cursor.fetchone()[0]
