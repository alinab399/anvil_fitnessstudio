import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def query_database_dict(query: str, *args):
  with sqlite3.connect(data_files["fitness_studio.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query, args).fetchall()
  return [dict(row) for row in result]


@anvil.server.callable
def get_studio_stats():
  sql = """
  SELECT Studio.Name, COUNT(Mitglied.MitgliedId) as anzahl 
  FROM Studio
  LEFT JOIN Mitglied ON Studio.Studionr = Mitglied.Studionr
  GROUP BY Studio.Name
  """
  return anvil.server.call('query_database_dict', sql)

@anvil.server.callable
def get_all_studios():
  sql = "SELECT * FROM Studio"
  return anvil.server.call('query_database_dict', sql)

@anvil.server.callable
def get_all_kurse(value):
  sql = """
    SELECT Kurs.Bezeichnung, Trainer.Name, Kurs.Dauer, Studio.Name AS Studio
    FROM Kurs
    JOIN Trainer ON Kurs.Personalnr = Trainer.Personalnr
    JOIN Studio ON Trainer.Studionr = Studio.Studionr
    WHERE Kurs.Bezeichnung = ?
    ORDER BY Kurs.Bezeichnung
  """
  return anvil.server.call('query_database_dict', sql, value)

@anvil.server.callable
def get_all_trainer(value):
  sql = """
    SELECT Kurs.Bezeichnung, Trainer.Name, Kurs.Dauer, Studio.Name AS Studio
    FROM Kurs
    JOIN Trainer ON Kurs.Personalnr = Trainer.Personalnr
    JOIN Studio ON Trainer.Studionr = Studio.Studionr
    WHERE Trainer.Name = ?
    ORDER BY Trainer.Name
  """
  return anvil.server.call('query_database_dict', sql, value)

@anvil.server.callable
def get_kurse_bezeichnung_distinct():
  sql = """
    SELECT DISTINCT Bezeichnung
    FROM Kurs
    ORDER BY Bezeichnung
  """
  return anvil.server.call('query_database_dict', sql)

@anvil.server.callable
def get_trainer_name_distinct():
  sql = """
    SELECT DISTINCT Name
    FROM Trainer
    ORDER BY Name
  """
  return anvil.server.call('query_database_dict', sql)
