from ._anvil_designer import StartseiteTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from plotly import graph_objects as go

class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.aktualisiere_diagramm()
    
  def aktualisiere_diagramm(self):
    stats = anvil.server.call('get_studio_stats')
    studio_labels = [str(r['Studionr']) for r in stats]
    mitglieder_counts = [r['anzahl'] for r in stats]

    self.diagramm_auslastung.layout = {
      'title': 'Mitglieder pro Studio',
      'xaxis': {'title': 'Studio Nummer'},
      'yaxis': {'title': 'Anzahl Mitglieder'}
    }

    self.diagramm_auslastung.data = [
      go.Bar(
        x = studio_labels,
        y = mitglieder_counts,
        marker = dict(color='#2196F3')
      )
    ]

  
