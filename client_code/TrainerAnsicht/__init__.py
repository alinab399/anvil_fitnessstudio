from ._anvil_designer import TrainerAnsichtTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TrainerAnsicht(TrainerAnsichtTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.filldatagrid()

    # Any code you write here will run before the form opens.
  def filldatagrid(self):
    self.repeating_panel_alleTrainer.items = anvil.server.call('get_all_trainer')

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')
