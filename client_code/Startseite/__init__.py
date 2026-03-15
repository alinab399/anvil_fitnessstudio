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
    self.fill_datagrid_studios()
    
  def aktualisiere_diagramm(self):
    stats = anvil.server.call('get_studio_stats')
    print(stats)
    studio_labels = [str(r['Name']) for r in stats]
    mitglieder_counts = [r['anzahl'] for r in stats]

    self.diagramm_auslastung.layout = {
      'title': 'Mitglieder pro Studio',
      'xaxis': {
        'title': 'Studio Name',
        'type': 'category'
      },
      'yaxis': {
        'title': 'Anzahl Mitglieder',
        'tickmode': 'auto'
      }
    }

    self.diagramm_auslastung.data = [
      go.Bar(
        x = studio_labels,
        y = mitglieder_counts,
        marker = dict(color='#2196F3'),
        text = mitglieder_counts
      )
    ]


  def fill_datagrid_studios(self):
    return_value = anvil.server.call('get_all_studios')
    self.repeating_panel_studios.items = return_value

  @handle("link_sudios", "click")
  def link_sudios_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.data_grid_studios.scroll_into_view(smooth=True)

  @handle("link_kurse", "click")
  def link_kurse_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('KursAnsicht')

  @handle("link_trainer", "click")
  def link_trainer_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('TrainerAnsicht')
    
    

  
