##
#     Project: Text Data Parser
# Description: View text data files with definitions.
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2016 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

from . import DefinedFields
from .constants import FILE_UI_MAIN
from .model_data import ModelData
from .gtkbuilder_loader import GtkBuilderLoader
from gi.repository import Gtk

class UIMain(object):
  def __init__(self, application, settings, parser, definitions_file, data_file):
    self.application = application
    self.settings = settings
    self.parser = parser
    self.fields = None
    self.current_row = 0
    self.loadUI()
    # Map each iter to a field name
    self.map_iters = {}
    # Load the definition file if provided
    if definitions_file:
      self.load_definitions(definitions_file)
    # Load the data file if provided
    if data_file:
      self.load_data(data_file)

  def load_definitions(self, definition_file):
    """Load the fields definitions file"""
    self.map_iters = {}
    self.fields = DefinedFields(definition_file)
    self.current_row = 0
    for field in self.fields:
      # Map each iter to a field name
      self.map_iters[field.name] = self.model.add_data(field, None)

  def load_data(self, data_file):
    """Load the data file using the parser"""
    self.parser.load_from_file(self.fields, data_file)
    if self.parser.data_file:
      with open(self.parser.data_file, 'r') as text_file:
        for line in text_file:
          self.ui.textbuffer.insert_at_cursor(line, len(line))
        text_file.close()
    
  def loadUI(self):
    """Load the interface UI"""
    self.ui = GtkBuilderLoader(FILE_UI_MAIN)
    self.model = ModelData(self.ui.list_data)
    self.ui.win_main.set_application(self.application)
    self.ui.textbuffer.connect("notify::cursor-position",
      self.on_textbuffer_cursor_position_changed)
    self._template_position = self.ui.label_position.get_text()
    # Update the cursor position
    self.on_textbuffer_cursor_position_changed(None, None)
    # Set the actions accelerator group
    for group_name in ('actions_data', 'actions_application'):
      for action in self.ui.get_object(group_name).list_actions():
        action.set_accel_group(self.ui.accelerators)
    # Connect signals from the glade file to the functions with the same name
    self.ui.connect_signals(self)

  def run(self):
    """Show the UI"""
    self.ui.win_main.show_all()

  def on_winMain_delete_event(self, widget, event):
    """Close the application"""
    self.ui.win_main.destroy()
    self.application.quit()

  def on_action_data_next_activate(self, action):
    """Move to the next record"""
    if self.current_row < len(self.parser) - 1:
      self.current_row += 1
      self.show_current_record()

  def on_action_data_previous_activate(self, action):
    """Move to the next record"""
    if self.current_row > 0:
      self.current_row -= 1
      self.show_current_record()

  def show_current_record(self):
    """Reload the current record fields"""
    value = self.parser[self.current_row]
    for field in self.fields:
      self.model.set_data(
        treeiter=self.map_iters[field.name],
        field=field,
        raw_value=value[field.name])

  def on_action_application_about_activate(self, action):
    """Show the about dialog"""
    pass

  def on_action_application_quit_activate(self, action):
    """Close the window"""
    self.ui.win_main.destroy()

  def on_textbuffer_cursor_position_changed(self, widget, property_name):
    """Update the cursor position"""
    iter = self.ui.textbuffer.get_iter_at_mark(
      self.ui.textbuffer.get_insert())
    self.ui.label_position.set_text(self._template_position % {
      'row': iter.get_line() + 1,
      'column': iter.get_line_offset() + 1})
