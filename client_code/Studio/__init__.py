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
    return_values = anvil.server.call('get_diagramm_pie_data', row_dict)
    self.fuelle_diagramm(return_values)
    

  def fuelle_diagramm(self, return_values):
    mitglieder_counts = [str(r['anzahl']) for r in return_values]
    kurs_bez = [r['Bezeichnung'] for r in return_values]

    self.plot_kurs.data = [
      go.Pie(
        labels = kurs_bez,
        values = mitglieder_counts,
        marker = dict(colors=['#8FCFF7','#8F96F7','#B38FF7','#CF8FF7','#E28FF7',])
      )
    ]

  def fuelle_datagridkurse(self, row_dict):
    return_values = anvil.server.call('get_kurs_trainer_data', row_dict)
    self.repeating_panel_kurse.items = return_values

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')
    
