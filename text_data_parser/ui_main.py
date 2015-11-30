##
#     Project: Text Data Parser
# Description: View text data files with definitions.
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2015 Fabio Castelli
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

from .defined_fields import DefinedFields
from .constants import FILE_UI_MAIN
from .functions import show_dialog_fileopen, _
from .settings import *
from .model_data import ModelData
from .gtkbuilder_loader import GtkBuilderLoader
from .ui_about import UIAbout
from gi.repository import Gtk

LINE_NUMBER_MARGIN = 1


class UIMain(object):
    def __init__(self, application, settings, parser, definitions, data):
        self.application = application
        self.settings = settings
        self.parser = parser
        self.fields = None
        self.current_row = -1
        self.total_rows = -1
        self.loadUI()
        self.about = UIAbout(self.ui.win_main, settings, False)
        # Restore the options from settings
        self.ui.action_settings_line_numbers.set_active(
            self.settings.get_setting(
                SETTING_SHOW_LINE_NUMBERS,
                self.ui.action_settings_line_numbers.get_active()))
        # Restore the saved size and position
        if self.settings.get_setting(SETTING_MAIN_WINDOW_WIDTH) and \
                self.settings.get_setting(SETTING_MAIN_WINDOW_HEIGHT):
            self.ui.win_main.set_default_size(
                self.settings.get_setting(SETTING_MAIN_WINDOW_WIDTH, -1),
                self.settings.get_setting(SETTING_MAIN_WINDOW_HEIGHT, -1))
        if self.settings.get_setting(SETTING_MAIN_WINDOW_LEFT) and \
                self.settings.get_setting(SETTING_MAIN_WINDOW_TOP):
            self.ui.win_main.move(
                self.settings.get_setting(SETTING_MAIN_WINDOW_LEFT),
                self.settings.get_setting(SETTING_MAIN_WINDOW_TOP))
        # Restore the splitter position
        if self.settings.get_setting(SETTING_MAIN_WINDOW_SPLITTER,
                                   self.ui.paned_main.get_position()):
            self.ui.paned_main.set_position(self.settings.get_setting(
                SETTING_MAIN_WINDOW_SPLITTER,
                self.ui.paned_main.get_position()))
        # Map each iter to a field name
        self.map_iters = {}
        # Load the definition file if provided
        if definitions:
            self.load_definitions(definitions)
        # Load the data file if provided
        if data:
            self.load_data(data)
        else:
            self.show_current_record()

    def load_definitions(self, definition_file):
        """Load the fields definitions file"""
        self.map_iters = {}
        self.fields = DefinedFields(definition_file)
        self.current_row = 0
        for field in self.fields:
            # Map each iter to a field name
            self.map_iters[field.name] = self.model.add_data(field, None)
        self.ui.action_data_open.set_sensitive(True)

    def load_data(self, data_file):
        """Load the data file using the parser"""
        self.parser.load_from_file(self.fields, data_file)
        if self.parser.data_file:
            self.ui.textbuffer.set_text('')
            self.total_rows = 0
            with open(self.parser.data_file, 'r') as text_file:
                for line in text_file.xreadlines():
                    self.total_rows += 1
                    line = unicode(line.decode(self.parser.encoding))
                    self.ui.textbuffer.insert_at_cursor(line, -1)
                text_file.close()
            # Add line numbers on the left side using the tag line_nr
            for line in xrange(self.total_rows):
                self.ui.textbuffer.insert_with_tags(
                    self.ui.textbuffer.get_iter_at_line(line),
                    ('%%%dd%%s' % len(str(self.total_rows))) % (
                        line + 1, ' ' * LINE_NUMBER_MARGIN),
                    self.ui.tag_line_nr)
            self.current_row = 0
            self.show_current_record()

    def loadUI(self):
        """Load the interface UI"""
        self.ui = GtkBuilderLoader(FILE_UI_MAIN)
        self.model = ModelData(self.ui.list_data)
        self.ui.win_main.set_application(self.application)
        self.ui.textbuffer.connect("notify::cursor-position",
                                   self.on_textbuffer_cursor_position_changed)
        self._template_position = self.ui.label_position.get_text()
        self._template_recordnr = self.ui.label_recordnr.get_text()
        # Update the cursor position
        self.on_textbuffer_cursor_position_changed(None, None)
        # Set the actions accelerator group
        for group_name in ('actions_data', 'actions_application'):
            for action in self.ui.get_object(group_name).list_actions():
                action.set_accel_group(self.ui.accelerators)
        # Connect signals from the glade file to the module functions
        self.ui.connect_signals(self)

    def run(self):
        """Show the UI"""
        self.ui.win_main.show_all()

    def on_winMain_delete_event(self, widget, event):
        """Save the settings and close the application"""
        # Window position
        position = self.ui.win_main.get_position()
        self.settings.set_setting(SETTING_MAIN_WINDOW_LEFT, position[0])
        self.settings.set_setting(SETTING_MAIN_WINDOW_TOP, position[1])
        # Window size
        size = self.ui.win_main.get_size()
        self.settings.set_setting(SETTING_MAIN_WINDOW_WIDTH, size[0])
        self.settings.set_setting(SETTING_MAIN_WINDOW_HEIGHT, size[1])
        # Splitter position
        self.settings.set_setting(SETTING_MAIN_WINDOW_SPLITTER,
                                  self.ui.paned_main.get_position())
        # Preferences
        self.settings.set_setting(
            SETTING_SHOW_LINE_NUMBERS,
            self.ui.action_settings_line_numbers.get_active())
        # Save settings and quit
        self.settings.save()
        self.about.destroy()
        self.ui.win_main.destroy()
        self.application.quit()

    def on_action_data_definitions_activate(self, action):
        """Select and load a definitions file"""
        selected_filename = show_dialog_fileopen(
            parent=self.ui.win_main,
            title=_("Select a definitions file to load"))
        if selected_filename:
            self.load_definitions(selected_filename)

    def on_action_data_open_activate(self, action):
        """Select and load a data file"""
        selected_filename = show_dialog_fileopen(
            parent=self.ui.win_main,
            title=_("Select a data file to load"))
        if selected_filename:
            self.load_data(selected_filename)

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
        if len(self.parser):
            value = self.parser[self.current_row]
            for field in self.fields:
                self.model.set_data(
                    treeiter=self.map_iters[field.name],
                    field=field,
                    raw_value=value[field.name])
            # Highlight the text line for the selected record
            iter_start = self.ui.textbuffer.get_iter_at_line(self.current_row)
            iter_end = self.ui.textbuffer.get_iter_at_line(
                self.current_row + 1)
            self.ui.textbuffer.remove_tag(self.ui.tag_highlight_line,
                                          self.ui.textbuffer.get_start_iter(),
                                          self.ui.textbuffer.get_end_iter())
            self.ui.textbuffer.apply_tag(self.ui.tag_highlight_line,
                                         iter_start, iter_end)

        self.ui.action_data_previous.set_sensitive(self.current_row > 0)
        self.ui.action_data_next.set_sensitive(
            self.current_row < len(self.parser) - 1)
        self.ui.label_recordnr.set_text(self._template_recordnr % {
            'record': self.current_row + 1})

    def on_action_application_about_activate(self, action):
        """Show the about dialog"""
        self.about.show()

    def on_action_application_quit_activate(self, action):
        """Close the window"""
        self.ui.win_main.destroy()

    def on_textbuffer_cursor_position_changed(self, widget, property_name):
        """Update the cursor position"""
        iter = self.ui.textbuffer.get_iter_at_mark(
            self.ui.textbuffer.get_insert())
        column_number = iter.get_line_offset() + 1
        column_number -= len(str(self.total_rows)) + LINE_NUMBER_MARGIN
        self.ui.label_position.set_text(self._template_position % {
            'row': iter.get_line() + 1,
            'column': column_number if column_number > 0 else 0
        })

    def on_action_settings_line_numbers_toggled(self, action):
        """Show or hide the line numbers"""
        self.ui.tag_line_nr.props.invisible = \
            not self.ui.action_settings_line_numbers.get_active()
