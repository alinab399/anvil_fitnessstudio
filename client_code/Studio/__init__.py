from ._anvil_designer import StudioTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go


class Studio(StudioTemplate):
  def __init__(self, row_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.label_studio_name.text = row_dict['Name']
    self.label_studio_address.text = row_dict['Adresse']
    self.daten_diagramm_holen(row_dict)
    self.fuelle_datagridkurse(row_dict)

  def daten_diagramm_holen(self, row_dict):
    sql = """
      SELECT Kurs.Bezeichnung, COUNT(besucht.KursId) AS anzahl
      FROM Kurs
      JOIN Trainer ON Kurs.Personalnr = Trainer.Personalnr
      LEFT JOIN besucht ON Kurs.KursId = besucht.KursId
      WHERE Trainer.Studionr = ?
      GROUP BY Kurs.Bezeichnung
    """
    return_values = anvil.server.call('query_database_dict', sql, row_dict['Studionr'])
    print(return_values)
    self.fuelle_diagramm(return_values)
    

  def fuelle_diagramm(self, return_values):
    mitglieder_counts = [str(r['anzahl']) for r in return_values]
    kurs_bez = [r['Bezeichnung'] for r in return_values]

    self.plot_kurs.data = [
      go.Pie(
        labels = kurs_bez,
        values = mitglieder_counts
      )
    ]

  def fuelle_datagridkurse(self, row_dict):
    sql = """
    SELECT Kurs.Bezeichnung, Trainer.Name, Kurs.Dauer 
    FROM Kurs
    JOIN Trainer ON Kurs.Personalnr = Trainer.Personalnr
    WHERE Trainer.Studionr = ?
    """

    return_values = anvil.server.call('query_database_dict', sql, row_dict['Studionr'])
  

    self.repeating_panel_kurse.items = return_values
    
