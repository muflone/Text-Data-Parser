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


class ModelData(object):
    COL_ID = 0
    COL_NAME = 1
    COL_DESCRIPTION = 2
    COL_START = 3
    COL_END = 4
    COL_LENGTH = 5
    COL_TYPE = 6
    COL_VALUE = 7
    COL_RAW = 8

    def __init__(self, model):
        self.model = model

    def clear(self):
        """Clear the model"""
        return self.model.clear()

    def add_data(self, field, raw_value):
        return self.model.append((
            len(self.model) + 1,
            field.name,
            field.description,
            field.start,
            field.end,
            field.length,
            field.type,
            field.decimals,
            str(self.get_value_from_raw(field, raw_value)),
            raw_value))

    def get_model(self):
        return self.model

    def set_data(self, treeiter, field, raw_value):
        self.model.set_value(treeiter, 1, field.name)
        self.model.set_value(treeiter, 2, field.description)
        self.model.set_value(treeiter, 3, field.start)
        self.model.set_value(treeiter, 4, field.end)
        self.model.set_value(treeiter, 5, field.length)
        self.model.set_value(treeiter, 6, field.type)
        self.model.set_value(treeiter, 7, field.decimals)
        self.model.set_value(treeiter, 8,
                             str(self.get_value_from_raw(field, raw_value)))
        self.model.set_value(treeiter, 9, raw_value)

    def get_value_from_raw(self, field, raw_value):
        if raw_value is None:
            value = ''
        else:
            try:
                if field.type == 'A':
                    value = raw_value.strip()
                elif field.type == 'D':
                    value = int(raw_value)
                elif field.type == 'S':
                    value = float(raw_value)
            except:
                value = 'Invalid value'
        return value
