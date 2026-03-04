from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.fill_datagrid_studios()
    # Any code you write here will run before the form opens.

  @handle("button_more", "click")
  def button_more_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
    
  def fill_datagrid_studios(self):
    return_value = anvil.server.call('get_all_studios')
    self.data_grid_studios.items = return_value
    print(return_value)

