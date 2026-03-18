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
    self.filldatagrid()
    # Any code you write here will run before the form opens.
    return_value = anvil.server.call('get_all_kurse')
    self.drop_down_KursAnsicht.items = return_value['Bezeichnung']

  def filldatagrid(self):
    self.repeating_panel_alleKurse.items = anvil.server.call('get_all_kurse')

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

  @handle("drop_down_KursAnsicht", "change")
  def drop_down_KursAnsicht_change(self, **event_args):
    """This method is called when an item is selected"""
    
