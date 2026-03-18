from ._anvil_designer import KursAnsichtTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class KursAnsicht(KursAnsichtTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    return_value = anvil.server.call('get_kurse_bezeichnung_distinct')
    kurs_namen = [r['Bezeichnung'] for r in return_value]
    self.drop_down_KursAnsicht.items = kurs_namen

    self.drop_down_KursAnsicht.selected_value = kurs_namen[0]
    self.filldatagrid(kurs_namen[0])

  def filldatagrid(self, value):
    self.repeating_panel_alleKurse.items = anvil.server.call('get_all_kurse', value)

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

  @handle("drop_down_KursAnsicht", "change")
  def drop_down_KursAnsicht_change(self, **event_args):
    """This method is called when an item is selected"""
    ausgewaehlt = self.drop_down_KursAnsicht.selected_value
    self.filldatagrid(ausgewaehlt)
    
