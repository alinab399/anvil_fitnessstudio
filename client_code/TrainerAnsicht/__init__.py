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
    return_value = anvil.server.call('get_trainer_name_distinct')
    trainer_namen = [r['Name'] for r in return_value]
    self.drop_down_TrainerAnsicht.items = trainer_namen

    self.drop_down_TrainerAnsicht.selected_value = trainer_namen[0]
    self.filldatagrid(trainer_namen[0])

    # Any code you write here will run before the form opens.
  def filldatagrid(self, value):
    self.repeating_panel_alleTrainer.items = anvil.server.call('get_all_trainer', value)

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

  @handle("drop_down_TrainerAnsicht", "change")
  def drop_down_TrainerAnsicht_change(self, **event_args):
    """This method is called when an item is selected"""
    ausgewaehlt = self.drop_down_TrainerAnsicht.selected_value
    self.filldatagrid(ausgewaehlt)
