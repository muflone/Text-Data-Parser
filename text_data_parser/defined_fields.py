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

from .defined_field import DefinedField


class DefinedFields(object):
    def __init__(self, s_filename):
        self.fields = {}
        self.iter_count = -1
        # Load the definition file
        with open(s_filename, 'r') as f:
            for s_line in f:
                self.add_field_from_definition_line(s_line)

    def add_field_from_definition_line(self, s_line):
        """Add a new field from a definition line"""
        # Strip invalid characters
        s_line = s_line.replace('\r', '')
        s_line = s_line.replace('\n', '')
        if '#' in s_line:
            s_line = s_line[0:s_line.index('#')]
        if s_line:
            # Get field definition
            s_name = s_line[0:12].strip()
            s_pos_start = s_line[12:20].lstrip()
            s_pos_end = s_line[20:26].lstrip()
            s_pos_length = s_line[26:32].lstrip()
            s_decimals = s_line[32:37].lstrip()
            s_type = s_line[41]
            s_description = s_line[45:].rstrip().decode('iso-8859-1')
            # Fix quirks
            if s_decimals == '':
                s_decimals = '0'
            elif int(s_decimals) == 0:
                s_type = 'D'
            # Create new field and add it to the fields list
            new_field = DefinedField(
                name=s_name,
                ftype=s_type,
                start=int(s_pos_start),
                end=int(s_pos_end),
                length=int(s_pos_length),
                decimals=int(s_decimals),
                description=s_description)
            self.fields[s_name] = new_field

    def __iter__(self):
        """Iterate over the fields sorted by their start position"""
        for field in sorted(self.fields.values(),
                            key=lambda field: field.start):
            yield field

    def __getitem__(self, index):
        return self.fields[index]

    def __len__(self):
        return len(self.fields)
